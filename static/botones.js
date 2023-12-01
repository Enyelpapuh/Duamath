var progreso = {{ progreso }};

document.addEventListener("DOMContentLoaded", function() {
    const miBoton = document.getElementById("miBoton");
    
    let valor = parseInt(miBoton.value);
    if (progreso <= valor) {
      miBoton.classList.add("block");
    }
  });