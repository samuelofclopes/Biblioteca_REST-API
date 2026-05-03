async function fazer_login() {

    // 1. Pega os valores do formulário
    // Declaração de constantes com os valores dos campos de entrada
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    // 2. Valida se estão preenchidos
    if (!username || !password) { // Em python seria "if not username or not password"
        document.getElementById("erro").innerText = "Todos os campos devem ser preenchidos."
        return
    } // Fechamos do if

    // 3. Envia pedido à API
    const response = await fetch("/api/auth/login", { // Estamos a usar o fetch para enviar um pedido POST para a rota de login da API
        method: "POST", // O método
        headers: { "Content-Type": "application/json" }, // Define o formato dos dados enviados como JSON
        body: JSON.stringify({ username, password }) // // Transformamos o objeto com credenciais para o formato string JSON
    })

    // 4. Pede e espera pela resposta da API
    const data = await response.json()

    // 5. Verifica se correu bem
    if (response.ok) { // Verifica se a resposta foi bem-sucedida (status 200-299) no caso, deverá ser 200 como definimos em python
        localStorage.setItem("token", data.token) // Guarda o token no localStorage do navegador para usar em outras páginas
        window.location.href = "/dashboard"        // Vai para o dashboard
    } else {
        document.getElementById("erro").innerText = data.error // Mostra erro
    }
}