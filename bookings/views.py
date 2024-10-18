# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Seat
from .forms import AdminLoginForm
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Home page to select event
def home_view(request):
    events = Event.objects.all()
    return render(request, 'bookings/home.html', {'events': events})

def seat_selection_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        selected_row = request.POST.get('row')
        selected_seat = request.POST.get('seat')

        # Fetch or create a seat with the selected row and seat number for the specific event
        seat, created = Seat.objects.get_or_create(event=event, row=selected_row, number=selected_seat)

        # Update seat details (regardless of previous status)
        seat.is_booked = True
        seat.booked_by = name
        seat.save()

        # Redirect to success page after submission
        return redirect('success_page')

    # Render seat selection form
    return render(request, 'bookings/seat_selection.html', {
        'event': event,
        'rows': range(1, 27),  # 26 rows
        'seats_numbers': range(1, 11),  # 10 seats per row
    })
    
      

def success_view(request):
    return render(request, 'bookings/success.html')


# Admin login view
def admin_login_view(request):
    next_url = request.GET.get('next')  # Capture the 'next' parameter if present
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username == "mohan" and password == "mohan123":
                # Check for the 'next' parameter
                if next_url:
                    return redirect(next_url)  # Redirect to 'next' if available
                else:
                    return redirect('event_creation')  # Default to admin dashboard
    else:
        form = AdminLoginForm()
    return render(request, 'bookings/admin_login.html', {'form': form})


# View for admin to create an event
def event_creation_view(request):
    if request.method == 'POST':
        name = request.POST.get('event_name')
        date = request.POST.get('event_date')
        event = Event.objects.create(name=name, date=date)
        
        # Create 260 seats (26 rows and 10 seats per row)
        for row in range(1, 27):
         for number in range(1, 11):
          Seat.objects.create(row=row, number=number, event=event, is_booked=False)  # Ensure is_booked=False
        
        return redirect('home')
    
    return render(request, 'bookings/event_creation.html')

@login_required
def admin_dashboard_view(request):
    # Ensure only the admin user sees this
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)

    return render(request, 'admin_dashboard.html')

@login_required
def seat_management_view(request):
    # Ensure only admin can access this
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)

    # Fetch all seats from the database
    seats = Seat.objects.all()

    return render(request, 'seat_management.html', {'seats': seats})

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from bookings.serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer  # Create a serializer for User

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'username': user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view."})
