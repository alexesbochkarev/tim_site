from main.forms import LegalUserRegistrationForm, PhysicalUserRegistrationForm, PasswordResetForm, UserLoginForm, AddPluginForm

def get_context_data(request):
    context = {
        'login': UserLoginForm(),
        'register_legal': LegalUserRegistrationForm(),
        'register_physical': PhysicalUserRegistrationForm(),
        'password_reset': PasswordResetForm(),
        'add_plugin': AddPluginForm()
    }
    return context