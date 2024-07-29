from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from userauths.models import Profile
from userauths.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import PasswordChangeView
from .forms import PatientForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from userauths.models import Profile, User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Notification, Patient, Results, Status
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

from tensorflow.keras.models import  Model, load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore 
import io
import base64
import tensorflow as tf
import numpy as np
from django.conf import settings
import os
import json
from PIL import Image
import matplotlib.pyplot as plt


model_path = os.path.join(settings.BASE_DIR, "models", "densenet_model_v3.h5")
model_path1 = os.path.join(settings.BASE_DIR, "models", "xgb_model_v2.h5")
model = load_model(model_path)
model1 = load_model(model_path1)


with open('./models/imagenet_classes.json', 'r') as f:
    labelInfo = json.load(f)

@login_required
def dashboard(request):
    
    notifications = Notification.objects.filter(user=request.user, seen=False)
    patients = Patient.objects.filter(user=request.user)
    total_noti = notifications.count()
    total_pat = patients.count()
    date = timezone.now().date() 
    ss = Status.objects.filter(user=request.user, type="Completed")
    context = {
        "total_noti":total_noti,
        "notifications":notifications,
        "total_pat":total_pat,
        "date":date,
        "ss":ss
    }
    
    return render(request, "user_dashboard/dashboard.html", context)

def notification_mark_as_seen(request, id):
    noti = Notification.objects.get(id=id)
    noti.seen = True
    noti.save()
    noti.delete()
    messages.success(request, "Notification Deleted")

    return redirect("user_dashboard:dashboard")


def search_patient(request):
    if request.method == "GET":
        query = request.GET.get("q")

    if query == "":
        query = None

    if query:
        patients = Patient.objects.filter(Q(lastname__icontains=query))

    context = {
        "patients":patients,
    }

    return render(request, "user_dashboard/records.html", context)





@login_required
def records(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)
    patients = Patient.objects.filter(user=request.user).order_by('-date')
    total_noti = notifications.count() 
    context = {
        "total_noti":total_noti,
        "patients":patients,
    }

    return render(request, "user_dashboard/records.html", context)


# Function to preprocess the input image
def preprocess_input_image(img_path):
    img = Image.open(img_path)
    img = img.resize((224, 224))  # Resize the image to the input size of your model
    img_array = np.array(img)
    if img_array.ndim == 2:  # Check if the image is grayscale
        img_array = np.stack((img_array,) * 3, axis=-1)  # Convert to 3 channels if grayscale
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize the image
    return img_array

# Function to get the Grad-CAM heatmap
def get_grad_cam_heatmap(model, img_array, last_conv_layer_name, pred_index=None):
    grad_model = Model([model.inputs], [model.get_layer(last_conv_layer_name).output, model.output])

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def save_grad_cam(img_path, heatmap, alpha=0.4):
    img = Image.open(img_path)
    img = img.resize((224, 224))

    heatmap = np.uint8(255 * heatmap)
    heatmap = Image.fromarray(heatmap)
    heatmap = heatmap.resize((img.size[0], img.size[1]))
    heatmap = np.array(heatmap)

    plt.imshow(img)
    plt.imshow(heatmap, cmap='jet', alpha=alpha)
    plt.axis('off')

    # Save heatmap to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buffer.seek(0)

    # Save the buffer content to a file
    img_filename = os.path.basename(img_path).split('.')[0] + '_heatmap.png'
    return ContentFile(buffer.read(), name=img_filename)

def process_image_and_predict(fileObj, results_instance):
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)
    testimage = '.' + filePathName

    img = image.load_img(testimage, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Create a batch

    # Normalize the image
    img_array /= 255.0

    # Make a prediction
    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction, axis=1)[0]  # Get the index from array
    predicted_class = labelInfo[str(predicted_index)]  # Convert index to string for lookup

    input_image = preprocess_input_image(testimage)

    # Generate the Grad-CAM heatmap
    heatmap = get_grad_cam_heatmap(model, input_image, last_conv_layer_name="conv5_block16_concat")

    # Save the Grad-CAM heatmap
    heatmap_image_content = save_grad_cam(testimage, heatmap)

    return filePathName, heatmap_image_content, predicted_class




@login_required
def add_patient(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)
    total_noti = notifications.count()

    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            
            # Retrieve the last count for the current user's patient
            last_result = Results.objects.all().order_by('-entry_count').first()
            current_count = last_result.entry_count + 1 if last_result else 1


            user_data = Results.objects.create(
                user=request.user,
                firstname = request.POST['firstname'],
                lastname = request.POST['lastname'],
                phone = request.POST['phone'],
                age = request.POST['age'],
                gender = request.POST['gender'],
                address = request.POST['address'],
                occupation = request.POST['occupation'],
                age_group_5_years=int(request.POST['age_group_5_years']),
                first_degree_hx=int(request.POST['first_degree_hx']),
                age_menarche=int(request.POST['age_menarche']),
                age_first_birth=int(request.POST['age_first_birth']),
                birads_breast_density=int(request.POST['birads_breast_density']),
                breast_cancer_history=int(request.POST['breast_cancer_history']),
                current_hrt=int(request.POST['current_hrt']),
                menopaus=int(request.POST['menopaus']),
                mammogram_image = form.cleaned_data['mammogram_image'],
                bmi_group=int(request.POST['bmi_group']),
                biophx=int(request.POST['biophx']),
                entry_count=current_count
            )
            
            user_data.save()
            messages.success(request, "Patient form filled successfully.")
            return redirect('user_dashboard:results')

            
            
    else:
        form = PatientForm()

    context = {
        "total_noti": total_noti,
        "form": form,
    }

    return render(request, "user_dashboard/add_patient.html", context)

@login_required
def results(request):
    # Retrieve the latest patient object for the current user
    patient = Patient.objects.filter(user=request.user).order_by('-date').first()

    if patient is None:
        messages.error(request, "No patient records found for the current user.")
        return redirect('user_dashboard:add_patient')

    # Retrieve the associated results object if it exists
    model_result = Results.objects.all().order_by('-entry_count').first()
    val = ""

    if model_result is None:
        messages.error(request, "No results found for the current patient.")
        return redirect('user_dashboard:add_patient')

    # Extract features from the latest results
    features = np.array([
        model_result.age_group_5_years,
        model_result.first_degree_hx,
        model_result.age_menarche,
        model_result.age_first_birth,
        model_result.birads_breast_density,
        model_result.breast_cancer_history,
        model_result.current_hrt,
        model_result.menopaus,
        model_result.bmi_group,
        model_result.biophx
    ]).reshape(1, 10)

    # Make a prediction
    prediction = model1.predict(features)
    predicted_index = np.argmax(prediction, axis=1)[0]
    
    # Determine the likelihood message
    if predicted_index == 0:
        value = "Not Likely"
    else:
        value = "Likely"
        list_features = features.flatten().tolist()
        if list_features.count(1) > 3:
            val = 'Highly likely'
        else:
            val = 'Less likely'

    # Handle the mammogram image processing
    if patient.mammogram_image:
        fileObj = patient.mammogram_image
        filePathName, heatmap_image, predicted_class = process_image_and_predict(fileObj, model_result)

        # Update the existing Patient object with prediction details
        patient.predicted_class = predicted_class
        patient.prediction_value = value
        patient.prediction_val = val
        
        # Save the heatmap image as a ContentFile object
        if heatmap_image:
            patient.heatmap_image.save('heatmap_image.png', heatmap_image)
        
        patient.save()
        
        state = Status.objects.create(
            user=request.user,
            firstname=patient.firstname,
            type="Completed",
            status_date=timezone.now().date()
        )
        state.save()
    else:
        filePathName = None
        heatmap_image = None
        predicted_class = None

    return render(request, "user_dashboard/result.html", 
    {
        "predicted_class": patient.predicted_class,
        "filePathName": filePathName,
        "heatmap_image": patient.heatmap_image.url if patient.heatmap_image else None,
        "value": patient.prediction_value,
        "val": val,
    })





def edit_records(request, pk):
    record = Patient.objects.get(id=pk)
    form = PatientForm(instance=record) 
    notifications = Notification.objects.filter(user=request.user, seen=False)
    total_noti = notifications.count() 
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient details was updated')
            return redirect('user_dashboard:records')
        
    context = {
        "total_noti":total_noti,
        "form":form,
        "record":record,
    }

    return render(request, 'user_dashboard/add_patient.html', context=context)

def delete_records(request, pk):
    record = Patient.objects.get(id=pk)

    record.delete()
    messages.success(request, 'Patient details was deleted')

    return redirect("user_dashboard:records")



@login_required
def view_invoice(request, pk):
    # Get the patient object
    patient = get_object_or_404(Patient, id=pk)

    # Fetch results using the patient's id
    #results_a = Results.objects.filter(patient=patient)

    context = {
        "patient": patient,
        
        "heatmap_image": patient.heatmap_image.url if patient.heatmap_image else None,
        
    }
    return render(request, "user_dashboard/invoice.html", context)

