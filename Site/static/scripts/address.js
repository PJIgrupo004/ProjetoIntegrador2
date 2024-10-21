function buscaCEP(cep) {
    let json_fetch = ''
    console.log(cep)
    const requestOptions = {
          method: "GET",
          redirect: "follow"
        };
        fetch(`https://brasilapi.com.br/api/cep/v2/${cep}`, requestOptions)
            .then(response => response.json())
            .then(data => {
                document.getElementById("estado").value = data.state;
                document.getElementById("cidade").value = data.city;
                document.getElementById("rua").value = data.street;
                document.getElementById("bairro").value = data.neighborhood;
                console.log(data);
            })
        .catch((error) => console.error(error));
    
}