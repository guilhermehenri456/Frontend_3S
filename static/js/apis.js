async function getGato() {
    let resultado = await fetch("https://api.thecatapi.com/v1/images/search")

    if (resultado.ok) {
        let dados = await resultado.json()
        render_gato(dados)

    }
}

function  render_gato(dados) {
    let urlImg = dados[0].url
    const imgGato = document.getElementById('img-gato')
    const iconGato = document.getElementById('icon-gato')

    iconGato.style.display = "none"
    imgGato.style.display = "block"
    imgGato.src = urlImg
}
async function getCachorro() {
    let resultado = await fetch("https://dog.ceo/api/breeds/image/random")

    if (resultado.ok) {
        let dados = await resultado.json()
        render_cachorro(dados)

    }
}

function  render_cachorro(dados) {
    let Img = dados.message
    const imgCachorro = document.getElementById('img-cachorro')
    const iconCachorro = document.getElementById('icon-cachorro')

    iconCachorro.style.display = "none"
    imgCachorro.style.display = "block"
    imgCachorro.src = Img
}

async function getRaposa() {
    let resultado = await fetch("https://randomfox.ca/floof")

    if (resultado.ok) {
        let dados = await resultado.json()
        render_raposa(dados)

    }
}

function  render_raposa(dados) {
    let Img = dados.image
    const imgRaposa = document.getElementById('img-raposa')
    const iconRaposa = document.getElementById('icon-raposa')

    iconRaposa.style.display = "none"
    imgRaposa.style.display = "block"
    imgRaposa.src = Img
}

