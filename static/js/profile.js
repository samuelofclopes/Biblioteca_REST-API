async function carregarPerfil() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    const resposta = await fetch('/api/auth/me', {
        headers: { 
            'Authorization': `Bearer ${token}` 
        }
    });

    if (!resposta.ok) {
        const erro = await resposta.json();
        console.error("Erro do servidor:", erro);
        return;
    }

    const dados = await resposta.json();
    document.getElementById('user').innerText = dados.user.username;
    document.getElementById('email').innerText = dados.user.email;
}