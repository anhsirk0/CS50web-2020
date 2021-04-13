# Final project - **Hotel booking system**

## About project
The project is a hotel booking system.  
It consists of 997 Hotels taken from makemytrip hotel database.  
User can search a city (**autocomplete** supported) and can sort through the search results. 

### Features overview
 - Responsive design
 - Search bar with autocomplete support
 - Dynamic elements
 - Pagination
 - Material design

#### 4 sorting methods are supported:
 - Rating (Ascending)
 - Price (Ascending)
 - Rating (Descending)
 - Price (Descending) 

User can Signup or book a hotel without signup
While Viewing a Hotel , user can view info, pictures, highlights, price, rating.  
When booking a hotel , user can select checkin date and checkout date and other details.  
Price for booking is created at front end and also at backend after submitting booking details

#### Details included for booking
 - Checkin date
 - Checkout date
 - Number of rooms
 - Number of kids
 - Number of Adults

#### Dynamic changes in booking details
 - Price changes dynamically as user select other fields.
 - Disabling of dates is also applied.
 - Checkout date can't be after checkin date.
 - Default checkout date is after one day of checkin date.
 - Maximum date of booking is one year in future.


## Detailed info about the project
This project has a single app 'book'
'book' app has several python files.

### helpers.py
this file contain some helper functions
info about the functions are as following
 1. get_highlights   
   this take a string input of highlights.   
   highlights are stored as a single string and separated by "|" .   
   it remove duplicates from highlights  and remove non alphanumeric characters.   
   it return a list of strings , later django loop over that list and display every highlight for the hotel. 
 2. get_imgurls  it return a list of strings , later django loop over that list and display every highlight.
   this take a string input of image urls .
   image urls are stored as a single string and separated by "|" .
   it return a list of strings , later django loop over that list and display every image for the hotel.
 3. get_stars  
   this take a string input of stars which are stored as 'x stars' where x can 0 to 5.  
   it return list 1s and 0s where count of 1s is the rating, later django loop over this and display gold star for each 1 and empty star for each 0.  

### models.py 
this file contain models for user hotel booking 
info about the models are as following

 1. User model  
   this is the base auth model inherited from AbstractUser class.  
   additional info about users are phone (IntegerField) & avatar - image url for users (CharField).  
 2. Hotel model   
   this is to store hotels . it contains following fields.  
    - city (city of hotel)
    - name (name of the hotel)
    - overview (description for hotel)
    - highlight (general highlights for hotel)
    - room_types (luxury or regural) 
    - rating (stars)  
    - price (base price)
    - imgurls (image urls)
 3. Booking model   
   this is to store a booking. it contains following fields.  
    - hotel (hotel object)
    - user (user object)
    - tracking_id (unique tracking ID)
    - first_name (users first name)
    - last_name (users last name)
    - email (email address of user)
    - phone (phone number of user)
    - room (no of rooms booked)
    - adult (no of adults booked)
    - child (no of children booked)
    - checkin_date (check in date)
    - checkout_date (check in date)


### urls.py  
this file contains url routes for the app
 - login
 - logout
 - register
 - cities (return JsonResponse of all cities)
 - search (search hotels)
 - popular (popular hotels)
 - profile (user profile )
 - book (booking page)
 - success (after a booking is successful)
 - track (track the booking with tracking_id)

  
### views.py  
function based views.   
 - index (basic homepage with few popular hotels) 
 - cities (return list of cities, for autocomplete inputs) 
 - search_hotels (for search and sort functionality pagination enabled)
 - popular hotels (high rated hotels , pagination enabled)
 - hotel_view (single hotel page)
 - create_price (generate price by hotel_id,room, no of adults,child,days)
 - book_hotel (POST request only ,book a hote withl)
 - successful (POST only, booking succesful page ,create a booking)
