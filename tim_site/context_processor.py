from main.forms import LegalUserRegistrationForm, PhysicalUserRegistrationForm, PasswordResetForm

def get_context_data(request):
    context = {
        'register_legal': LegalUserRegistrationForm(),
        'register_physical': PhysicalUserRegistrationForm(),
        'password_reset': PasswordResetForm()
    }
    return context