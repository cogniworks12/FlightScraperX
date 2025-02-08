# FlightScraperX

## **Project Overview**
FlightScraperX is a **multi-threaded flight data scraper** that efficiently extracts real-time flight details from airline websites and APIs. The project is built using **Object-Oriented Programming (OOP) principles**, making it modular, scalable, and easy to maintain.

## **Features**
 Multi-threaded scraping for high-speed data extraction  
 Real-time flight details including departure, arrival, price, and availability  
 OOP-based design for modular and reusable code  
 Clean and maintainable architecture  
 Data storage in CSV/JSON format for easy access  

## **Installation**
To set up and run the scraper, follow these steps:

### **1. Clone the Repository**
```bash
git clone https://github.com/cogniworks12/FlightScraperX.git
cd FlightScraperX
```

### **2. Create and Activate a Virtual Environment**
```bash
python3 -m venv env
source env/bin/activate  # For Linux/macOS
env\Scripts\activate  # For Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run the Scraper**
```bash
python scraper.py
```

## **Usage**
1. Configure your **search parameters** (e.g., departure city, destination, date range) in the script.
2. Run `scraper.py` to start the scraping process.
3. The extracted flight data is saved in **JSON format**.

## **Supported Data Fields**
The scraper retrieves and structures flight details, including:
-  **Flight Number**
-  **Departure & Arrival Cities**
-  **Departure & Arrival Times**
-  **Ticket Prices & Fare Classes**
-  **Airline Information**
-  **Availability & Updates**

## **Code Structure & OOP Implementation**
- **Encapsulation**: Data handling and scraping logic are wrapped in reusable classes.  
- **Abstraction**: High-level methods hide implementation details, improving readability.  
- **Inheritance**: Base classes provide reusable functionalities for different airline scraping implementations.  
- **Polymorphism**: Methods are designed to handle different flight search formats dynamically.  

## **Contributing**
We welcome contributions! Feel free to submit **pull requests** or **open issues** to suggest improvements.

## **License**
This project is licensed under the **MIT License**.

---
**Author:** Cogniworks.ai  
🔗 [GitHub](https://github.com/cogniworks12)  
🚀 Optimized for structured and scalable flight data extraction

