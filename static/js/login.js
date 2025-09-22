document.addEventListener('DOMContentLoaded', function() {
    const loginFormUser = document.getElementById('loginFormUser');

    loginFormUser.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(loginFormUser);
        fetch('/login/usuarios', {
            method: 'POST',
            body: formData
        }).then(function(response) {
            if (response.ok) {
                    window.location.href = '/user_dashboard.html';
            } else {
                alert('Erro ao realizar login.');
            }
        }).catch(function(error) {
            alert('Erro ao realizar login.');
        });
    });
});