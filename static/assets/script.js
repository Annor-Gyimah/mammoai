const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');
const profileCont = document.getElementById('profile-cont')
const changeProfile = document.getElementById('change-profile')

allSideMenu.forEach(item => {
    const li = item.parentElement;

    item.addEventListener('click', function () {
        allSideMenu.forEach(i=> {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});

const menuBar = document.querySelector('#content nav .fa.fa-bars');
const sideBar  = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
    sideBar.classList.toggle('hide');
})


const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .fa');
const searchForm  = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
        e.preventDefault();
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchButtonIcon.classList.replace('fa-search', 'fa-times');
        }else {
            searchButtonIcon.classList.replace('fa-times', 'fa-search');
        }
    }
})



if (window.innerWidth < 768) {
    sideBar.classList.add('hide');
}else if (window.innerWidth > 576) {
    searchButtonIcon.classList.replace('fa-times', 'fa-search');
    searchForm.classList.remove('show');
}


window.addEventListener('resize', function () {
    if (this.innerWidth > 576) {
        searchButtonIcon.classList.replace('fa-times', 'fa-search');
        searchForm.classList.remove('show');
    }
})

document.addEventListener('click', function(event){
    if (event.target.classList.contains('profile-img')){
        if(profileCont.classList.contains('hidden')){
            profileCont.classList.remove('hidden')
        }else{
            profileCont.classList.add('hidden')
        }
    }else if (!event.target.classList.contains('profile-cont') && !event.target.classList.contains('user-profile')){
        if(!profileCont.classList.contains('hidden')){
            profileCont.classList.add('hidden')
        }
    }

    
});