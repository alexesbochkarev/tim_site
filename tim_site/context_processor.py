from main.forms import LegalUserRegistrationForm, PhysicalUserRegistrationForm, PasswordResetForm, UserLoginForm

def get_context_data(request):
    context = {
        'login': UserLoginForm(),
        'register_legal': LegalUserRegistrationForm(),
        'register_physical': PhysicalUserRegistrationForm(),
        'password_reset': PasswordResetForm()
    }
    return context