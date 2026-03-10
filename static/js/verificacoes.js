// var nome = prompt("como voce chama?")
//
//
// if (nome == null) {
//     alert("recarregue a pagina")
// } else {
//     let correto = confirm("voce se chama " + nome + "?")
//
//
//     if (correto) {
//         alert(nome + " bem vindo ao site de cursos")
//     } else {
//         alert("recarregue a pagina")
//     }
// }

function limpaInputsLogin() {
    const inputEmail = document.getElementById('input-email')
    const inputSenha = document.getElementById('input-senha')

    inputEmail.value = ''
    inputSenha.value = ''
}

document.addEventListener("DOMContentLoaded", function () {
    const formLogin = document.getElementById('form-login')


    formLogin.addEventListener("submit", function (event) {
        // pegar os dois inuputs do formulario
        const inputEmail = document.getElementById('input-email')
        const inputSenha = document.getElementById('input-senha')


        let temErro = false


        // verificar se os inputs estao vazios
        if (inputEmail.value === '') {
            inputEmail.classList.add('is-invalid')
            temErro = true
        } else {
            inputEmail.classList.remove('is-invalid')
        }


        if (inputSenha.value === '') {
            inputSenha.classList.add('is-invalid')
            temErro = true
        } else {
            inputSenha.classList.remove('is-invalid')
        }


        if (temErro) {
            // evita de enviar o formulario
            event.preventDefault()
            alert("preencha todos os campos")
        }


    })
})
