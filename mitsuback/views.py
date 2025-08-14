from django.shortcuts import render
from .models import Register, WinningList
from .serializers import RegisterSerializer, WinningListSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import random
# Create your views here.

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user(request):
    register = Register.objects.all()
    serializer = RegisterSerializer(register, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_initials(request):
    """
    Get all registered users' first name initials in an array
    """
    users = Register.objects.all()
    initials = []
    
    for user in users:
        if user.full_name:
            # Split the full name and get the first name initial
            first_name = user.full_name.split()[0] if user.full_name.strip() else ""
            if first_name:
                initial = first_name[0].upper()
                initials.append(initial)
    
    return Response({
        'initials': initials,
        'count': len(initials)
    })

@api_view(['POST'])
def select_winner_by_initial(request):
    """
    Select a winner based on the provided initial
    Accepts initial in form data and returns a randomly selected winner
    """
    initial = request.data.get('initial', '').strip().upper()
    
    if not initial:
        return Response({
            'error': 'Initial is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if len(initial) != 1:
        return Response({
            'error': 'Initial must be a single character'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Find all users whose first name starts with the given initial
    # Exclude users who have already won for this initial
    matching_users = []
    for user in Register.objects.all():
        if user.full_name:
            first_name = user.full_name.split()[0] if user.full_name.strip() else ""
            if first_name and first_name[0].upper() == initial:
                # Check if user has already won for this initial
                existing_winner = WinningList.objects.filter(user=user, initial=initial).first()
                if not existing_winner:
                    matching_users.append(user)
    
    if not matching_users:
        return Response({
            'error': f'No users found with initial "{initial}"',
            'initial': initial,
            'matching_users_count': 0
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Add all matching users to the winning list
    # (All matching_users are already filtered to exclude previous winners)
    winners_added = []
    for user in matching_users:
        winner_entry = WinningList.objects.create(user=user, initial=initial)
        winners_added.append(winner_entry)
    
    # Randomly select one winner from the matching users
    selected_winner = random.choice(matching_users)
    
    # Get or create the winning entry for the selected winner
    winner_entry, created = WinningList.objects.get_or_create(
        user=selected_winner, 
        initial=initial
    )
    
    # Get previous winners for this initial
    previous_winners = WinningList.objects.filter(initial=initial).exclude(user=selected_winner)
    
    return Response({
        'message': f'Winner selected for initial "{initial}"',
        'initial': initial,
        'matching_users_count': len(matching_users),
        'winners_added_count': len(winners_added),
        'selected_winner': {
            'id': selected_winner.id,
            'full_name': selected_winner.full_name,
            'email': selected_winner.email,
            'employee_id': selected_winner.employee_id
        },
        'all_matching_users': [
            {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'employee_id': user.employee_id
            } for user in matching_users
        ],
        'previous_winners_count': previous_winners.count(),
        'previous_winners': [
            {
                'id': winner.user.id,
                'full_name': winner.user.full_name,
                'email': winner.user.email,
                'employee_id': winner.user.employee_id,
                'won_at': winner.won_at
            } for winner in previous_winners
        ]
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_winners(request):
    winners = WinningList.objects.all()
    serializer = WinningListSerializer(winners, many=True)
    return Response(serializer.data)    