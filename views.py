# JJJs/views.py
#  from multiprocessing import AuthenticationError
from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .forms import  CustomUserCreationForm, BookingForm, CustomAuthenticationForm
from .models import Hostel, Booking, Area


# # Home view
def HomeView(request):
    return render(request, 'home.html')

# View for user registration
def register_view(request):
    """
    View for the registration page.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# View for user login
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    def get(self, request):
        # Render the login form
        return render(request, 'login.html')

    def post(self, request):
        # Handle the form submission
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # Login the user
            login(request, user)
            return redirect('dashboard')
        else:
            # Show an error message if login fails
            return render(request, 'login.html', {'error': 'Invalid credentials'})

# View for listing hostels
class ViewHostels(ListView):
    def get(self, request):
        # Fetch all hostels
        hostels = Hostel.objects.all()
        return render(request, 'view_hostels.html', {'hostels': hostels})

# View for hostel details
class DetailsView(DetailView):
    def get(self, request, hostel_name):
        # Fetch the hostel details based on the name
        hostel = get_object_or_404(Hostel, name=hostel_name)
        return render(request, 'details.html', {'hostel': hostel})

# View for booking a hostel
@login_required
class BookingView(BookingForm):
    def book_hostel(request):
        if request.method == 'POST':
            # Handle the booking form submission
            hostel_name = request.POST['hostel_name']
            entry_date = request.POST['entry_date']
            hostel = get_object_or_404(Hostel, name=hostel_name)
            area = Area.objects.filter(hostel=hostel).first()  # Assuming an area is associated with the hostel
            
            # Create a new booking
            booking = Booking.objects.create(
                hostel=hostel,
                area=area,
                user=request.user,
                entry_date=entry_date
            )
            booking.save()

            # Decrement the number of rooms
            hostel.number_of_rooms -= 1
            hostel.save()

            # Redirect to the booking success page
            return redirect('booking_success')
        else:
            # Render the booking form
            hostels = Hostel.objects.all()
            return render(request, 'book_hostel.html', {'hostels': hostels})

# View for booking success

def booking_success(request):
    # Render the booking success message
    return render(request, 'booking_success.html')

# Dashboard view
@login_required
def dashboard(request):
    # Fetch the user's bookings
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'bookings': bookings})

@login_required
def LogoutView(request):
    return render(request, 'logout.html')
