// colores
verde= '#209f64'
rojo= '#e83749'
amarillo= '#e7ba27'
azul= '#3498db'
gris= '#829294'

function eliminarAcento(input) {
  input.addEventListener('input', () => {
    input.value = input.value.replace(/´/g, '');
    input.value = input.value.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  });
}

/* validar cédula */
/* Solo números */
function numberOnly() {
    let nameInput = document.querySelectorAll('.solonumeros');
    nameInput.forEach((input) => {
      input.addEventListener('keydown', (e) => {
          const allowedKeys = [
          "Backspace", "Tab", "Enter", 
          "ArrowLeft", "ArrowUp", "ArrowRight", "ArrowDown",
          "Delete"
          ];
          
          const key = e.key;
          const isNumber = /^[0-9]$/.test(key);

          // 1. Permitir F5 (solo o con Ctrl)
          if (key === "F5") {
            return;
          }

          // 2. Permitir Ctrl + A (seleccionar todo)
          if (e.ctrlKey && (key === "a" || key === "A" || key === "c" || key === "C" || key === "v" || key==="V")) {
            return;
          }

          if (
              isNumber ||
              allowedKeys.includes(key)
          ) {
              return; // Permitir
          } else {
              e.preventDefault();
          }
      });
  });
}

/* Solo texto */
function alphaOnly() {
    let nameInput = document.querySelectorAll('.solotexto');
    nameInput.forEach((input) => {
      input.addEventListener('keydown', (e) => {
          const allowedKeys = [
              "Backspace", "Tab", "Enter", "ArrowLeft", "ArrowUp", "ArrowRight", "ArrowDown",
              " ", // espacio
              "Delete"
          ];
          const key = e.key;
          const isLetter = /^[a-zA-Z]$/.test(key);

          // 1. Permitir F5 (solo o con Ctrl)
          if (key === "F5") {
            return;
          }

          // 2. Permitir Ctrl + A (seleccionar todo)
          if (e.ctrlKey && (key === "a" || key === "A" || key === "c" || key === "C" || key === "v" || key==="V")) {
            return;
          }

          if (
              isLetter ||
              allowedKeys.includes(key)
          ) {
              // Permitir
              return;
          } else {
              e.preventDefault();
          }
      });
  });
}

/* Solo email (caracteres válidos para email) */
function emailOnly() {
    let emailInputs = document.querySelectorAll('.soloemail');
    
    emailInputs.forEach((input) => {
        input.addEventListener('keydown', (e) => {
            const allowedKeys = [
                "Backspace", "Tab", "Enter", "ArrowLeft", "ArrowUp", "ArrowRight", "ArrowDown",
                ".", "@", "-", "_", "+", "Delete"
            ];
            const key = e.key;

            // 1. Detectar atributos del input
            const esInstitucional = input.dataset.institucional === "true";
            const esSoloUsuario = input.dataset.usuario === "true"; // Lógica para bloquear @

            // 2. Ajustar la expresión regular
            const regexValidacion = esInstitucional ? /^[a-zA-Z]$/ : /^[a-zA-Z0-9]$/;
            const isLetterOrNumber = regexValidacion.test(key);

            // 3. Permitir F5
            if (key === "F5") return;

            // 4. Permitir Ctrl + A, C, V, X
            if (e.ctrlKey && /^[acvx]$/i.test(key)) return;

            // 5. Lógica de bloqueo de caracteres
            // Bloqueamos el @ si el campo tiene data-usuario="True"
            if (esSoloUsuario && key === "@") {
                e.preventDefault();
                return;
            }

            // Validar si el carácter es permitido
            if (isLetterOrNumber || allowedKeys.includes(key)) {
                return;
            } else {
                e.preventDefault();
            }
        });
    });
}

numberOnly();
alphaOnly();
emailOnly();


// Convertir en mayúsculas sin perder la posición del cursor
$(document).on("input", ".upper", function () {
  const $this = $(this);
  const start = $this[0].selectionStart;
  const end = $this[0].selectionEnd;
  
  $this.val($this.val().toUpperCase());
  
  // Restaurar la posición del cursor
  $this[0].setSelectionRange(start, end);
});

//CSRF TOKEN
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function bloquearInputs(e){
  const inputs = document.querySelectorAll(".solonumeros, .solotexto, .soloemail, .input");

inputs.forEach(input => {
  // Elimina el ´ y los retira de los caracteres
  eliminarAcento(input);

  // Bloquear pegar con mouse (clic derecho → pegar)
  //input.addEventListener("paste", function(e) {
    //e.preventDefault();
  //});

  // Bloquear arrastrar y soltar texto dentro del input
  input.addEventListener("drop", function(e) {
    e.preventDefault();
  });

  // Bloquear el menú contextual (clic derecho)
  //input.addEventListener("contextmenu", function(e) {
    //e.preventDefault();
  //});
});
}
bloquearInputs();


//Contraseñas
$(document).ready(function() {
    // Contraseñas
    const $inputPassword1 = $("#password");
    const $inputPassword2 = $("#confirmPassword");
    const $divErrorRegex = $("#divErrorRegex");
    const $divErrorPassword = $("#divErrorPassword");
    const $formResetPassword = $("#formResetPassword");

    const regex = /^(?=.*[a-zñáéíóúü])(?=.*[A-ZÑÁÉÍÓÚÜ])(?=.*\d)(?=.*[@$!%*?&.#,()\-])[A-Za-zñáéíóúü\d@$!%*?&.#,()\-\s]{8,64}$/;
    
    function validarContraseñas() {
        let esValido = true;
        const val1 = $inputPassword1.val();
        const val2 = $inputPassword2.val();

        // Evaluar complejidad en Campo 1
        if (!regex.test(val1)) {
            if (val1 !== "") {
                $inputPassword1.addClass("border-red-500");
                $divErrorRegex.text("¡Formato incorrecto! Mínimo 8 caracteres, 1 mayúscula, 1 minúscula, 1 número y 1 símbolo.");
                esValido = false;
            } else {
                $inputPassword1.removeClass("border-red-500");
                $divErrorRegex.text("");
            }
        } else {
            $inputPassword1.removeClass("border-red-500");
            $divErrorRegex.text("");
        }

        // Evaluar coincidencia en Campo 2
        if (val1 !== val2) {
            if (val2 !== "") {
                $inputPassword2.addClass("border-red-500");
                $divErrorPassword.text("Las contraseñas no coinciden.");
                esValido = false;
            } else {
                $inputPassword2.removeClass("border-red-500");
                $divErrorPassword.text("");
            }
        } else {
            $inputPassword2.removeClass("border-red-500");
            $divErrorPassword.text("");
        }

        return esValido;
    }

    // Mostrar/ocultar contraseña al hacer clic en el botón del ojo (global para vistas que lo usen)
    $(document).on("click", ".togglePassword", function() {
        const targetId = $(this).data("target");
        const $input = $("#" + targetId);
        const $icon = $(this).find("i");

        if ($input.attr("type") === "password") {
            $input.attr("type", "text");
            $icon.removeClass("bi-eye").addClass("bi-eye-slash");
        } else {
            $input.attr("type", "password");
            $icon.removeClass("bi-eye-slash").addClass("bi-eye");
        }
    });

    $(document).on("blur", ".password:not(#formLogin .password)", validarContraseñas);

    if ($formResetPassword.length) {
        $formResetPassword.on("submit", function(e) {
            if (!validarContraseñas()) {
                e.preventDefault();
            }
        });
    }
});


// SweetAlert2
function sAlert(tags, texto){
      // Determinar el icono según la etiqueta del mensaje
      let cleanTag = tags.replace('alert-', '').trim();
      let iconType, titleText, buttonColor;

      switch (cleanTag) {
        case 'success':
          iconType = 'success';
          titleText = '¡Éxito!';
          sColor =  verde;
          break;
        case 'danger':
          iconType = 'error';
          titleText = 'Error';
          sColor = rojo;
          break;
        case 'warning':
          iconType = 'warning';
          titleText = 'Advertencia';
          sColor =  amarillo;
          break;
        case 'info':
          iconType = 'info';
          titleText = 'Información';
          sColor = azul;
          break;
        default:
          // Para etiquetas personalizadas o 'debug' - corregido a 'info'
          iconType = 'info';
          titleText = 'Aviso';
          sColor = gris;
      }

      Swal.fire({
        icon: iconType,
        iconColor: sColor,
        title: titleText, 
        text: texto,
        timer: 2500,
        timerProgressBar: true,
        showConfirmButton: true,
        confirmButtonText: 'Aceptar',
        confirmButtonColor: sColor,
        background: '#f5efef',
        color: '#3d3d3d',
        backdrop: '#343a4075',
        padding: '2em',
        customClass: {
          popup: 'shadow-lg border-radius-xl',
          title: 'fw-bold',
        }
      });

      // --- AÑADIR PAUSA EN HOVER ---
      // Esperamos a que el popup se cree (SweetAlert lo hace asíncrono)
      setTimeout(() => {
        const popup = Swal.getPopup();
        if (popup) {
          const pausar = () => {
            if (Swal.getTimerLeft && Swal.getTimerLeft() > 0) {
              Swal.stopTimer();
            }
          };
          const reanudar = () => {
            if (Swal.getTimerLeft && Swal.getTimerLeft() > 0) {
              Swal.resumeTimer();
            }
          };

          // Detectar si el mouse ya está sobre el popup al momento de agregar el listener
          if (popup.matches(':hover')) {
            pausar();  // Si ya está hover, pausar inmediatamente
          }

          popup.addEventListener('mouseenter', pausar);
          popup.addEventListener('mouseleave', reanudar);
        }
      }, 100);
} // Pequeño retraso para asegurar que el DOM esté listo


// Función sConfirm modificada (no es necesario retornar nada)
function sConfirm(elemento, titulo, texto) {
    $elemento = $(elemento);
    
    Swal.fire({
        title: titulo,
        text: texto,
        icon: 'warning',
        showCancelButton: true,
        background: '#f5efef',
        color: '#3d3d3d',
        confirmButtonColor: '#28a745',  // verde (ajusta según tu variable)
        cancelButtonColor: '#dc3545',   // rojo
        confirmButtonText: 'Confirmar Acción',
        cancelButtonText: 'Regresar',
        backdrop: '#343a4075',
        padding: '2em',
        customClass: {
            popup: 'shadow-lg border-radius-xl',
            title: 'fw-bold',
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Marcar como confirmado y enviar el formulario
            $elemento.data('confirmed', true);
            // Envío manual: esto disparará el evento nuevamente,
            // pero ahora data('confirmed') es true, por lo que el dejará continuar.
            if ($elemento[0].tagName === "FORM"){
              $elemento.submit();
            }
            else if ($elemento[0].tagName === "BUTTON"){
              $elemento.click();
            }
        }
    });
}