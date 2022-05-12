
async function get_cupcakes(){
    // Retrieves list of cupcakes for api
    const response = await axios.get('http://127.0.0.1:5000/api/cupcakes')

    for(let cupcake of response.data.cupcakes){
        option = display_cupcakes_HTML(cupcake)
        $('#cupcake-list').append(option)
    }
}

function display_cupcakes_HTML(obj) {

    return `<div id='cupcake${obj.id}'>
    <p> Flavor: ${obj.flavor} | Size: ${obj.size} | Rating: ${obj.rating}</p>
    </div> `
}

$('#cupcake-form').on('submit', async function (evt) {
    evt.preventDefault();

    let flavor = $("#flavor").val();
    let rating = $("#rating").val();
    let size = $("#size").val();
    let image = $("input[name='size']").val();

    const newCupcakeResponse = await axios.post("http://127.0.0.1:5000/api/cupcakes", {
      flavor,
      rating,
      size,
      image
    });

    let newCupcake = $(display_cupcakes_HTML(newCupcakeResponse.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#cupcake-form").trigger("reset");
  });


get_cupcakes()
