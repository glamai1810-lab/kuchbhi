document.getElementById('churnForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Hardcoding static values for fields not in our simplified UI form 
    // to satisfy the API's Pydantic model requirements.
    const payload = {
        gender: "Female",
        SeniorCitizen: 0,
        Partner: "No",
        Dependents: "No",
        tenure: parseInt(document.getElementById('tenure').value),
        PhoneService: "Yes",
        MultipleLines: "No",
        InternetService: "Fiber optic",
        OnlineSecurity: "No",
        OnlineBackup: "No",
        DeviceProtection: "No",
        TechSupport: "No",
        StreamingTV: "No",
        StreamingMovies: "No",
        Contract: document.getElementById('Contract').value,
        PaperlessBilling: "Yes",
        PaymentMethod: "Electronic check",
        MonthlyCharges: parseFloat(document.getElementById('MonthlyCharges').value),
        TotalCharges: parseFloat(document.getElementById('TotalCharges').value)
    };

    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        const resultCard = document.getElementById('resultCard');
        
        // Reset classes
        resultCard.className = ''; 
        
        if(result.risk_level === "High Risk") resultCard.classList.add('high-risk');
        else if(result.risk_level === "Medium Risk") resultCard.classList.add('medium-risk');
        else resultCard.classList.add('low-risk');

        document.getElementById('riskLevel').innerText = result.risk_level;
        document.getElementById('probValue').innerText = result.probability;

    } catch (error) {
        alert("Error connecting to the API. Make sure the FastAPI backend is running.");
        console.error(error);
    }
});
