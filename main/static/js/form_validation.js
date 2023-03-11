$.validator.methods.email = function( value, element ) {
  return this.optional( element ) || /[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+/.test( value );
}


 $("#formValidation").validate({
  rules:{
    first_name:{
      required: true
    },
    last_name:{
      required: true
    },
    patronymic:{
      required: true
    },
    email: {
      email:true
    },
    email1: {
      equalTo : "#email_id-1"
    },
    password1: {
        required: true
    },
    password2 : {
      equalTo : "#pass_id-1"
    }

  },
  messages: {
     first_name: {
        required: "Заполните это поле",
     },
     last_name: {
        required: "Заполните это поле",
     },
     patronymic: {
        required: "Заполните это поле",
     },
     email: "Введён некоректный email",
     email1: "Email не совпадают",
     password1: {
        required: "Введите пароль"
     },
     password2:"Пароли не совпадают"

  },

  submitHandler: function(form) {
    form.submit();
  }
 });


 $("#formValidationLegal").validate({
  rules:{
    first_name:{
      required: true
    },
    last_name:{
      required: true
    },
    patronymic:{
      required: true
    },
    email: {
      email:true
    },
    email1: {
      equalTo : "#id_email"
    },
    password1: {
        required: true
    },
    password2 : {
      equalTo : "#id_password1"
    },
    organization_type:{
      required: true
    },
    organization_name:{
      required: true
    },
    organization_address:{
      required: true
    },
    INN:{
      required: true,
      minlength:10,
      maxlength:10
    },
    KPP:{
      required: true,
      minlength:9,
      maxlength:9
    }

  },
  messages: {
     first_name: {
        required: "Заполните это поле",
     },
     last_name: {
        required: "Заполните это поле",
     },
     patronymic: {
        required: "Заполните это поле",
     },
     email: "Введён некоректный email",
     email1: "Email не совпадают",
     password1: {
        required: "Введите пароль"
     },
     password2:"Пароли не совпадают",
     organization_type: {
        required: "Заполните это поле",
     },
     organization_name: {
        required: "Заполните это поле",
     },
     organization_address: {
        required: "Заполните это поле",
     },
     INN: {
        required: "Заполните это поле",
        minlength:"ИНН состоит из 10 цифр",
        maxlength:"ИНН состоит из 10 цифр"
     },
     KPP: {
        required: "Заполните это поле",
        minlength:"КПП состоит из 9 цифр",
        maxlength:"КПП состоит из 9 цифр"
     },

  },

  submitHandler: function(form) {
    form.submit();
  }
 });


