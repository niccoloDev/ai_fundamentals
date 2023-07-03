# ai_fundamentals
## Repository for the AI Fundamentals Course's Project

## How to use
After cloning, cd into the project folder and run
``docker compose up``
The web application will be available on port 5000 (http://evolutrade:5000 or http://localhost:5000).

# EvoluTrade: A Web-Based Tool for Stock Portfolio Generation using an Evolutionary Algorithm
## AI Fundamentals Project
### Niccolò Califano
### July 2023

## Introduction
EvoluTrade is a web-based tool for stock portfolio generation designed for academic purposes. The application, realized as a project for a university exam, implements an evolutionary algorithm from scratch, uses Flask as its web framework, and includes various libraries for form validation and real-time client-server communication.

## Related Works
Many existing tools for portfolio optimization utilize traditional techniques like Modern Portfolio Theory (MPT). However, the application of evolutionary algorithms in this field, particularly within a real-time, interactive web-based framework, remains less explored. In this context, EvoluTrade serves as a pedagogical exploration of these concepts.

## Methodologies
EvoluTrade employs a Model-View-Controller (MVC) architectural pattern, facilitating separation of concerns.

### Back-end
The back-end is built with Python and Flask, which handle HTTP request processing and routing. Flask-WTForms is employed for form data handling, validation, and rendering. The PortfolioGenerator class, which resides in the business_logic module, encapsulates the core functionality of portfolio generation using an evolutionary algorithm.

The algorithm is implemented without the aid of third-party libraries. It initiates with an initial population of potential portfolios, then calculates the fitness of each portfolio based on the Sharpe ratio - a simple formula given by: ( Expected portfolio return - Risk-free rate ) / Portfolio standard deviation.


This fitness measure, while straightforward, is a simplification of the complexities involved in real-world portfolio optimization and is used here purely for illustrative purposes.

Following fitness evaluation, an evolutionary loop begins, iterating for a set number of generations. Each iteration involves selection, crossover, and mutation operations, generating a new population. The optimal portfolio is updated and tracked throughout the evolution.

### Front-end
The front-end is constructed with HTML, CSS, and JavaScript, Bootstrap for responsive design, and Jinja2 for HTML templification. jQuery is employed for DOM manipulation and event handling, while Chart.js is used for pie chart visualization of asset distribution. Flask-SocketIO is utilized to enable real-time, bidirectional communication between the client and the server.

## Assessment
EvoluTrade offers a valuable learning experience in the balance of computational complexity and real-time feedback within a web application. The evolutionary algorithm, though simplified for the sake of this project, offers an intriguing exploration into potential methods of portfolio optimization. Meanwhile, the use of Flask-SocketIO for real-time updates offers an engaging user experience, providing insights into the iterative nature of the evolutionary process.

## Conclusion
In conclusion, EvoluTrade is an instructive example of the application of AI and evolutionary computation to finance. It provides a simplified, yet interactive, tool for stock portfolio generation, showcasing the potential of evolutionary algorithms in this field. While it is not designed for commercial or professional use, it serves as a useful educational tool for exploring the intersection of artificial intelligence, web development, and financial portfolio management.


