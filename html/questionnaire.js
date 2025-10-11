const api_url = "http://127.0.0.1:8000/generate";

async function handleAPI(){
    const prompt = document.getElementById("inputTest").value;
    var response = document.getElementById("resultado");

    const data = {prompt};

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
        response.textContent = result.response;
    } catch(error){
        console.error('Erro: ', error)
    }
}