// Função para validar o formato de tempo
function validateTime(value) {
    const timePattern = /^([01]\d|2[0-3]):([0-5]\d)$/; // Padrão de hora (HH:MM)
    return timePattern.test(value); // Retorna true se o formato estiver correto
}

// Função para validar um número dentro de um intervalo
function validateNumber(value, min, max) {
    const number = Number(value); // Converte o valor para número
    return !isNaN(number) && number >= min && number <= max; // Verifica se o número está no intervalo
}

// Espera até que o documento esteja carregado
document.addEventListener('DOMContentLoaded', function () {
    // Obtém o formulário pelo ID e verifica se existe antes de adicionar o listener
    const form = document.getElementById('psqi-form');
    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault(); // Impede o envio padrão do formulário

            let isValid = true; // Variável para rastrear se o formulário é válido

            // Limpa as mensagens de erro existentes
            form.querySelectorAll('.error-message').forEach(span => span.textContent = '');

            // Validação dos campos obrigatórios
            form.querySelectorAll('[required]').forEach(element => {
                const errorMessage = document.getElementById(`${element.id}-error`); // Obtém o span de erro correspondente

                if (errorMessage) { // Verifica se o span de erro existe antes de manipulá-lo
                    if (!element.value) { // Verifica se o campo está vazio
                        isValid = false;
                        element.style.border = '2px solid red'; // Adiciona estilo de erro
                        errorMessage.textContent = 'Este campo é obrigatório.'; // Exibe mensagem de erro
                    } else if (element.type === 'time' && !validateTime(element.value)) { // Valida o campo de tempo
                        isValid = false;
                        element.style.border = '2px solid red'; // Adiciona estilo de erro
                        errorMessage.textContent = 'Formato de hora inválido.'; // Exibe mensagem de erro
                    } else if (element.type === 'number' && !validateNumber(element.value, 0, 24)) { // Valida o campo de número
                        isValid = false;
                        element.style.border = '2px solid red'; // Adiciona estilo de erro
                        errorMessage.textContent = 'Número fora do intervalo permitido.'; // Exibe mensagem de erro
                    } else {
                        element.style.border = ''; // Remove o estilo de erro se estiver correto
                    }
                }
            });

            // Exibe uma mensagem dependendo da validade do formulário
            if (isValid) {
                form.submit(); // Envia o formulário se estiver válido
            } else {
                alert('Por favor, preencha todos os campos obrigatórios corretamente.');
            }
        });
    } else {
        console.error('Formulário com ID "psqi-form" não foi encontrado.');
    }
});
