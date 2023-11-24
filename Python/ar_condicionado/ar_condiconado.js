const form = document.getElementsByTagName("form")[0];
const  consumoAparelhoEl = form["consumo"]
const  horasPorDiaEl = form["horasPorDia"]
const  diasDeUsoEl = form["diasDeUso"]
const  precoDaEnergiaEl = form["precoDaEnergia"]
const  botaoCalcularEl = form["botao-calcular"]

function calculaGastos(evt){
    evt.preventDefault();
    const consumoAparelho = consumoAparelhoEl.value.replace(",",".");
    const consumoDiarioAparelho = consumoAparelho/30;
    const horasDiariasUso = horasPorDiaEl.value.replace(",",".");
    const diasUsoMes = diasDeUsoEl.value;
    const precoEnergia = precoDaEnergiaEl.value.replace(",",".");

    const custo = consumoDiarioAparelho * horasDiariasUso * diasUsoMes * precoEnergia;
    const consumoEl = document.getElementById("gasto");

    consumoEl.innerText = custo.toFixed(2)
}

botaoCalcularEl.addEventListener("click", calculaGastos);