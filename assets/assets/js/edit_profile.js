function logout() {
    window.location.href = '/login/'; // Adjust URL as needed
}

function uploadCoverPhoto(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('coverPhoto').src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
}

function uploadProfilePicture(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profilePictureLarge').src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
}

document.getElementById('sidebarToggle').addEventListener('click', function() {
    document.getElementById('sidebar-left').classList.toggle('active');
});
