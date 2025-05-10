https://github.com/rdabbs88/afleetingmoment/tree/main

https://afleetingmoment.vercel.app/
---
# **Fleeting Moments**

**Team Members:**

* Ryan Dabbs
* Jinson Jimmy
* Wyland On

---

## **Overview**

**Fleeting Moments App:** The idea is to allow users to post about their “fleeting moments.” These are brief moments that leave a lasting impression. This app would be a place where people can post anonymously (or not), describe how their moment went, what impact it has had, where the moment occurred, and with whom the moment was shared. This can act as a platform for students to express themselves and share core memories that they make throughout life.

All moments are publicly viewable, and a highlight feature is the interactive map showing where each moment took place.

---

## **Registration and Login**

* Modify username and password
* View past posts
* Link username to posts and comments when posting publicly

---

## **Forms**

* **Login/Logout**

  * Prompts for a valid username and password to authenticate users
* **Register**

  * Asks for a username and password and stores them in the users collection
* **Update Username**

  * Allows authenticated users to change their username
* **Update Profile Picture**

  * Lets users upload or change their profile image
* **Comment**

  * Enables users to interact with posts via comments (login required to link comment to user account)
* **Post a Moment**

  * Allows authenticated users to post a moment, enter text, and choose whether to remain anonymous

---

## **Blueprints**

### **Users**

* `/register`
  Allows a user to create an account by entering their name, email, username, password, and profile information. Usernames must be unique.
* `/login`
  Authenticates a user and redirects them to the index page. Displays an error if login fails.
* `/logout`
  Logs the user out.
* `/account`
  Displays the user's account/profile information.

### **Moments**

* `/`
  The index or explore page where users can search for posts.
* `/createmoment`
  Page with a form for users to create and submit a new moment.
* `/moment/<post_id>`
  Page shown when a user views or interacts with a specific moment.
* `/comment/<post_id>`
  Endpoint for submitting a comment on a moment.
* `/search`
  Allows users to search for posts by user, location, or keywords.

---

## **Database**

We define **User**, **Moment**, and **Comment** classes in a `models.py` file (separate from Blueprints).

* **User class/information:**
  `username`, `email`, `hashed_password`, `profile_picture`

* **Moment class/information:**
  `created_at` (time), `addressed_to` (recipient), `username` (or anonymous), `content` (description), `location` (geolocation as an array), `comments`

* **Comment class/information:**
  `created_at` (time), `content`, `username` (or anonymous), `moment_id` (reference to associated moment)

We will have a separate collection for users, one for moments, and another for comments.

---

## **API Integration**

We will use the **Google Maps API** to retrieve and store the user's geolocation. This will allow us to display moments on a map, helping users explore posts by location and connect with others nearby.
