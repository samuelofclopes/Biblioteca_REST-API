// 1. Função para buscar e listar os livros
async function carregarLivros() {
    try {
        const token = localStorage.getItem("token");
        
        // Proteção extra: se não houver token, nem tenta o fetch
        if (!token) {
            window.location.href = "/login";
            return;
        }
        const response = await fetch("/api/items", {
            headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
        });
        if (response.status === 401) {
            window.location.href = "/login";
            return;}
        const livros = await response.json();

        const tabela = document.getElementById("livros-lista");
        tabela.innerText = ""; // Limpa a tabela antes de popular

        livros.forEach(livro => {
            tabela.innerHTML += `
                <tr>
                    <td>${livro.title}</td>
                    <td>${livro.author}</td>
                    <td>${livro.available_copies}</td>
                </tr>
            `;
        });

    } catch (error) {
        console.error("Erro ao carregar livros:", error);
    }
}

// 2. Função de Logout
function logout() {
    localStorage.removeItem("token"); // Apaga o token
    window.location.href = "/login";   // Redireciona para o login


}

function ver_perfil() {
    window.location.href = "/profile";   // Redireciona para o perfil
}
// Executa ao carregar a página
carregarLivros();