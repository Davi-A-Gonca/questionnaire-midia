const api_url = "http://127.0.0.1:8000/generate";

function startQuestionnaire(){
    const botao = document.getElementById("botao");
    const container = document.getElementById("container");
    const start = document.getElementById("inputResposta");
    const response = document.getElementById("resultado");

    response.innerHTML = "<p>carregando</p>"
    start.value = "Olá, estou pronto para começar o questionário";
    handleAPI();
    botao.style.display = 'none';
    container.style.display = 'block';
}

async function handleAPI(){
    const input = document.getElementById("inputResposta");
    const prompt = input.value;
    const response = document.getElementById("resultado");
    const session_id = "teste";

    const data = {prompt, session_id};

    try{
        const resposta = await fetch(api_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        });

        if(!resposta.ok){
            throw new Error(`Erro: ${resposta.status}`);
        }

        const result = await resposta.json();
        resultHtml = "<p>" + result.response.replace(/\n/g, "<br>") + "</p>";
        response.innerHTML = resultHtml;
    } catch(error){
        console.error('Erro: ', error)
    }
    input.value = "";
}