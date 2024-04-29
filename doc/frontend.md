# detectaive

## startpage.vue
### Template Structure

Game Container (game-container): The main container for the component elements.
Title (title): Displays the game title with a typing animation effect.
Start Game Button (start-button): Initiates the game by navigating to the game modes screen.
Sign-in Button (sign-in-button): Manages user sign-in and sign-out actions.

### Data Properties

typedTitle: A string that displays the game's title with a typing animation.
titleStyle: An object containing CSS properties to style the title.
startButtonStyle: An object containing CSS properties to style the start game button.
signinButtonStyle: An object containing CSS properties to style the sign-in button.
signInOut: A string that toggles between "Sign In" and "Sign Out" based on the user's authentication status.

### Methods

mounted: Automatically types out the game title upon loading and checks for user authentication status to update the sign-in button text.
typeTitle(title, recursive): Creates a typing effect for the provided title. If recursive is true, the title re-types itself after a brief delay.
startGame(): Uses Vue Router to navigate to the game modes page.
signIn(): Handles user authentication. If no user is signed in, it initiates a sign-in process. If a user is signed in, it processes sign-out.

### Authentication Flow

Sign In: Utilizes Firebase's signInWithPopup to authenticate users via Google. On successful authentication, it stores user data in sessionStorage and optionally sends it to a backend server.
Sign Out: Clears user session data and updates UI to reflect the signed-out state.

### External Resources and Dependencies

Fonts: Uses the 'Anta' font imported from Google Fonts to maintain a consistent typographic style.
axios: Used for HTTP requests (e.g., posting user data to the backend).
firebase/auth: Provides authentication services, used for managing user sign-in and sign-out.


## multiplayer (leaderboard)
### Template Structure

Game Container (game-container): The main container that holds all UI elements, styled dynamically via gameContainerStyle.
Title (title): Displays the title of the game with a typing effect, styled by titleStyle.
Question Box: A text input field that allows users to enter their questions, styled to fit within the game container.

### Data Properties

userQuestion: A string that binds to the question input field, allowing the component to capture and handle user input.
typedTitle: A string that represents the title displayed at the top of the game container, which appears with a typing effect.
gameContainerStyle: An object containing CSS properties for styling the game's main container.
titleStyle: An object containing CSS properties for styling the title.

### Methods

mounted(): When the component is mounted, it immediately begins the typing animation for the title "story prompt: It is Jake's birthday today. His dog died in the afternoon."
typeTitle(title): Animates the typing of the given title string. The animation simulates typing at a controlled pace.
submitQuestion(): Captures the user's input when they press enter and logs it to the console. This method is meant to be expanded with functionality to handle the question, such as sending it to a backend service or processing it within the component.

### CSS Animations

typing: Progressively increases the width of the typing-effect span from 0 to 100%, creating the effect of text being typed.
blink: Toggles the border color of the typing-effect span between white and transparent, simulating a blinking cursor.


## modes.vue

### Template Structure

Game Container: A central container that holds all elements of the game's start screen.
Title: Displays a dynamically typed game title using the typing-effect style.
Start Game Button: Initiates the game by navigating to the game mode selection screen.
Sign-in Button: Allows the user to sign in or sign out using Google authentication.

### Data Properties

typedTitle: Stores the title that appears with a typing animation.
titleStyle: Contains the CSS styles for the title, positioning it centrally.
startButtonStyle: Defines the CSS for the start button, including positioning and styling.
signinButtonStyle: Similar to the start button, this defines the CSS for the sign-in button.
signInOut: Text displayed on the sign-in button, toggles between "Sign In" and "Sign Out" based on user status.

### Methods

mounted(): Invokes the typeTitle method to animate the game title and sets the sign-in button label based on session storage indicating user status.
typeTitle(title, recursive): Implements a typing effect for the title. If recursive is true, the animation restarts after a brief pause.
startGame(): Uses Vue Router to navigate to the game modes screen.
signIn(): Manages user authentication. If the user is not signed in, it initiates a sign-in process using Google authentication. If signed in, it handles sign-out.

### Authentication Flow

Sign In: Uses Firebase to authenticate with Google. On successful authentication, stores user information in session storage and optionally in a backend database. Updates the UI to reflect the user's signed-in status.
Sign Out: Clears user information from session storage and updates the UI to reflect the user's signed-out status.

### API Endpoints

User data storage: POST http://127.0.0.1:5000/api/store_user
This endpoint is called to store authenticated user information in the backend.

### Error Handling

Handles errors related to the sign-in and sign-out processes, including Firebase errors such as wrong credentials or network issues.

### External Resources and Dependencies

Google Fonts: Uses the 'Anta' font family imported from Google Fonts for consistent typography across the component.
axios: Used for HTTP requests to the backend.
firebase/auth: Provides the authentication functionality via Firebase.


## Singleplayer.vue

### Template Structure

Game Container: A div that houses the entire game interface, styled dynamically with gameContainerStyle.
Title: Displays the game's title with a typing effect animation.
Question Box: An input field where users can type their questions. It appears only if the question limit has not been reached.
Question Log: Lists all past questions and responses.
Change Prompt Button: Allows users to reset the game and fetch a new story prompt.

### Data Properties

questionLimit: Maximum number of questions allowed (default 10).
questionLog: Array that stores the history of questions and responses.
userQuestion: Models the input field for user questions.
typedTitle: Stores the currently displayed title with typing effect.
responseData: Stores response data from the server.
gameContainerStyle: Defines the CSS styles for the game container dynamically.
titleStyle: Defines the CSS styles for the title display.

### Computed Properties, Watchers, and Lifecycle Hooks

questionLimitReached: Checks if the number of questions asked has reached the questionLimit.
questionLimitReached: Redirects the user to a losing page when the question limit is reached.
mounted(): Fetches a new prompt from the backend and sets a session storage item upon component mounting.

### Methods

fetchNewPrompt(): Fetches a new story prompt from a specified backend endpoint, resetting necessary data.
typeTitle(title): Animates the typing of the title character by character.
submitQuestion(): Submits the user's question to the backend, handles the response, and updates the log.
saveQuestionLog(): Saves the question log to local storage.
scrollToBottom(): Scrolls the question log container to the bottom.
fetchNewPromptAndReset(): Clears local storage and fetches a new prompt.

### API Endpoints and Dependencies

Fetch prompt: GET https://cs370projectbackend-0t8f5ewp.b4a.run/single_player
Submit question: POST https://cs370projectbackend-0t8f5ewp.b4a.run/single_player/question
axios: Used for HTTP requests to the backend.
Vue Router: Used for routing actions like navigating to the losing page.

## winningPage.vue & losingPage.vue
### Template Structure

Game Container (game-container): The main container for the game-over interface, which is styled dynamically to cover the entire viewport.
Title: A message informing the player that they did/did not solve the mystery, styled to be centrally positioned.
Play Again Button: A button that allows players to restart the game.

### Data Properties

gameContainerStyle: Defines the CSS properties for the game container, ensuring it fills the viewport and uses a specific background color.
titleStyle: Sets the CSS properties for the title, positioning it centrally and styling the font to be visually impactful.

### Method

playAgain(): Utilizes Vue Router to navigate back to the game modes selection screen, allowing the player to try solving the mystery again.

### CSS Details

Game Container: Ensures that the container is relative, filling the entire viewport height, with overflow hidden to maintain cleanliness of the UI.
Title Style: Places the title centrally within the viewport using absolute positioning and CSS transforms. Text styling includes white color, large font size, and a specific font family to match the game's aesthetic.
Play Again Button: The button is styled for usability and aesthetics with padding, font styling, and a subtle box-shadow for depth. It includes a hover state that changes the background color to indicate interactivity.
