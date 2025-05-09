
# RannNetra.AI – Overclocked

RannNetra.AI is an advanced AI-driven solution designed to enhance battlefield operations by providing real-time threat detection, medical response optimization, and secure routing for combat units. This system aims to address critical challenges in modern warfare, including delayed medical responses, fragmented battlefield intelligence, and insecure communications.

## 🚀 Features

- **Real-Time Threat Detection**: Continuously monitors and identifies potential threats on the battlefield using advanced AI algorithms.
- **Medical Response Optimization**: Facilitates rapid identification and prioritization of injured personnel, ensuring timely medical assistance.
- **Secure Routing**: Calculates and suggests secure and efficient routes for troop movements, minimizing exposure to threats.
- **Integrated Dashboard**: Provides a comprehensive visual interface for commanders to monitor battlefield dynamics and make informed decisions.

## 🧠 Problem Statement

In critical combat situations, delays in identifying and reaching injured personnel can lead to preventable fatalities due to the lack of real-time triage and routing support. Additionally, the absence of real-time threat detection and fragmented battlefield intelligence hampers unified situational awareness for command units. Existing systems often rely on insecure or static communication lines, exposing troop movements to interception or miscoordination.

## 🛠️ Tech Stack

- **Frontend**: React.js, Tailwind CSS  
- **Backend**: Python (FastAPI), PostgreSQL  
- **Machine Learning**: TensorFlow, Scikit-learn  
- **Deployment**: Vercel  
- **Mapping & Visualization**: Mapbox, D3.js  

## 📂 Project Structure

```
RannNetra-Overclocked/
├── backend/
│   ├── api.py
│   └── utils/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── IntroSection.jsx
│   │   ├── MapSection.jsx
│   │   ├── StaticImageSection.jsx
│   │   ├── SatelliteMapSection.jsx
│   │   └── AnalyticsSection.jsx
│   ├── App.jsx
│   ├── App.css
│   └── main.jsx
├── README.md
└── requirements.txt
```

## 🌐 Deployment

Access the live application here: [RannNetra.AI](https://rannnetra.vercel.app/)

## 📽️ Demo Video

Watch the demonstration video here: [Google Drive Link](https://drive.google.com/drive/folders/1NBJm5o43FexihyRDu-6KLnwpIeoWgmxw?usp=sharing)

## 🚀 Getting Started

### Prerequisites

- Node.js (v14 or above)
- Python 3.8+
- PostgreSQL

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MokkshKapur/RannNetra-Overclocked.git
   cd RannNetra-Overclocked
   ```

2. **Install frontend dependencies:**

   ```bash
   cd src
   npm install
   ```

3. **Start the frontend development server:**

   ```bash
   npm run dev
   ```

4. **Set up the backend:**

   - Navigate to the `backend` directory.
   - Create a virtual environment and activate it.
   - Install the required Python packages:

     ```bash
     pip install -r requirements.txt
     ```

   - Run the FastAPI server:

     ```bash
     uvicorn api:app --reload
     ```

## 🤝 Contributing

We welcome contributions to RannNetra.AI! To contribute:

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature/YourFeature
   ```

3. Commit your changes:

   ```bash
   git commit -m 'Add YourFeature'
   ```

4. Push to the branch:

   ```bash
   git push origin feature/YourFeature
   ```

5. Open a pull request.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📫 Contact

- **Email**: mokkshkapur@gmail.com  
- **LinkedIn**: [Mokksh Kapur](https://www.linkedin.com/in/mokkshkapur/)  
- **GitHub**: [MokkshKapur](https://github.com/MokkshKapur)
