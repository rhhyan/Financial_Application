// Função para pegar as transações e exibir na página
async function carregarTransacoes() {
    const usuario_id = 1;  // Exemplo de ID de usuário
    const response = await fetch(`/saldo?usuario_id=${usuario_id}`);
    const data = await response.json();
    const saldo = data.saldo;

    document.getElementById('transacoes').innerHTML = `
        <p>Saldo atual: R$ ${saldo}</p>
    `;
}

// Função para registrar uma transação
document.getElementById('formTransacao').addEventListener('submit', async (event) => {
    event.preventDefault();

    const valor = document.getElementById('valor').value;
    const categoria = document.getElementById('categoria').value;
    const tipo = document.getElementById('tipo').value;
    const descricao = document.getElementById('descricao').value;
    const usuario_id = document.getElementById('usuario_id').value;

    const response = await fetch('/registrar_transacao', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            valor: parseFloat(valor),
            categoria: categoria,
            tipo: tipo,
            descricao: descricao,
            usuario_id: parseInt(usuario_id),
            data: new Date().toISOString().split('T')[0]  // Data no formato YYYY-MM-DD
        })
    });

    if (response.ok) {
        alert('Transação registrada com sucesso!');
        carregarTransacoes(); // Atualiza as transações após o registro
    } else {
        alert('Erro ao registrar transação');
    }
});

// Carregar as transações na inicialização
window.onload = carregarTransacoes;