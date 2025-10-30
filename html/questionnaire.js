const api_url = "http://127.0.0.1:8000/generate";

function startQuestionnaire(){ // Função para começar a conversa
    //Pegando elementos necessários para a função
    const botao = document.getElementById("botao");
    const container = document.getElementById("container");
    const start = document.getElementById("inputResposta");
    const response = document.getElementById("resultado");

    response.innerHTML = "<p>carregando</p>" //Informativo que está carregando a conversa
    start.value = "Olá, estou pronto para começar o questionário"; //Primeira mensagem para começar a conversa
    handleAPI(); //Chama função de conversa
    botao.style.display = 'none'; //Desapareçe com o botão
    container.style.display = 'block'; //Aparece a interface para conversa
}

async function handleAPI(){ //Função para conversar com a IA
    //Pegando elementos necessários para a função
    const input = document.getElementById("inputResposta");
    const prompt = input.value;
    const response = document.getElementById("resultado");
    const session_id = "teste"; //ID padrão para a conversa,
    // poderia colocar nome/email/senha do usuário para uma personalização mais específica

    const data = {prompt, session_id}; //Classe para enviar mensagem, igual a que está na API

    try{
        //Função para conversar com a IA
        const resposta = await fetch(api_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        });

        if(!resposta.ok){
            throw new Error(`Erro: ${resposta.status}`); //Erro para recibo falho
        }

        const result = await resposta.json(); //transforma a resposta em JSON
        resultHtml = "<p>" + result.response.replace(/\n/g, "<br>") + "</p>"; //Monta resposta
        response.innerHTML = resultHtml; //Mostra resposta na interface
    } catch(error){
        console.error('Erro: ', error)
    }
    input.value = "";//Zera input colocado pelo usuário
}