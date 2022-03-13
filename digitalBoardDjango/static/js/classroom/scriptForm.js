var inputs = document.querySelectorAll( 'input[type=text]' );
for (i = 0; i < inputs.length; i ++) {
  var inputEl = inputs[i];
  if( inputEl.value.trim() !== '' ) {
  	inputEl.parentNode.classList.add( 'input--filled' );
  }
  inputEl.addEventListener( 'focus', onFocus );
  inputEl.addEventListener( 'blur', onBlur );
}

function onFocus( ev ) {
  ev.target.parentNode.classList.add( 'inputs--filled' );
}

function onBlur( ev ) {
  if ( ev.target.value.trim() === '' ) {
  	ev.target.parentNode.classList.remove( 'inputs--filled' );
  } else if ( ev.target.checkValidity() == false ) {
    ev.target.parentNode.classList.add( 'inputs--invalid' );
    ev.target.addEventListener( 'input', liveValidation );
  } else if ( ev.target.checkValidity() == true ) {
    ev.target.parentNode.classList.remove( 'inputs--invalid' );
    ev.target.addEventListener( 'input', liveValidation );
  }
}

function liveValidation( ev ) {
  if ( ev.target.checkValidity() == false ) {
    ev.target.parentNode.classList.add( 'inputs--invalid' );
  } else {
    ev.target.parentNode.classList.remove( 'inputs--invalid' );
  }
}

var submitBtn = document.querySelector( 'input[type=submit]' );
submitBtn.addEventListener( 'click', onSubmit );

function onSubmit( ev ) {
  var inputsWrappers = ev.target.parentNode.querySelectorAll( 'span' );
  for (i = 0; i < inputsWrappers.length; i ++) {
    input = inputsWrappers[i].querySelector( 'input[type=text],' );
    if ( input.checkValidity() == false ) {
      inputsWrappers[i].classList.add( 'inputs--invalid' );
    } else if ( input.checkValidity() == true ) {
      inputsWrappers[i].classList.remove( 'inputs--invalid' );
    }
  }
}