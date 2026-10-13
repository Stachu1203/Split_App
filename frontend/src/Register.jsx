import { useState } from "react";

function Register(){
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const [info, setInfo] = useState('');

    const handleRegister = async (e) => {
    
      e.preventDefault();
      const response = await fetch('http://127.0.0.1:5000/api/register',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({username: login, password: password}), 
    });

    const data = await response.json();
    if (response.ok){
        setInfo(data.message);
    }
    else{
        setInfo(data.error)
    }
    
    }

    return (
        <>
            <form onSubmit={handleRegister}>
                <input value={login} type="text" onChange={(e) => setLogin(e.target.value)}/>
                <input value={password} type="password" onChange={(e) => setPassword(e.target.value)}/>
                <button type="submit">Zarejestruj</button>
            </form>
            <p>{info}</p>
        </>
    )
}

export default Register;