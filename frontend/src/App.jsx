import { useState } from "react"

function App() {
  const mockData = [
    {
        "id": 1,
        "payer": "Anna",
        "total_amount": 150.0,
        "borrowers": [
            { "name": "Bartek", "owes": 100.0 },
            { "name": "Michal", "owes": 50.0 }
        ]
    },
    {
        "id": 2,
        "payer": "Bartek",
        "total_amount": 60.0,
        "borrowers": [
            { "name": "Anna", "owes": 60.0 }
        ]
    }
  ];

  const [transactions, setTransactions] = useState([]);

  const handleCalculate = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/splitapp',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(mockData), 
    });
  
    const data = await response.json();

    setTransactions(data);
  };

   



  return (
    <>
      <h1>SPLIT_APP</h1>
      {transactions.map((e,ind) => (
        <p key = {ind}>{e.from} przelewa {e.amount} dla {e.to}</p>
      ))}
      
      <button onClick={handleCalculate}>Rozlicz</button>
    </>
  )
}

export default App
