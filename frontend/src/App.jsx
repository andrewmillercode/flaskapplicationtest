import React,{useState,useEffect} from "react"
import Button from "./myButton.jsx"
import axios from "axios";

function App() {

  const [profileData, setProfileData] = useState(null)

  function getData() {
    axios({
      method: "GET",
      url:"http://localhost:5000/flaskFunction",
    })
    .then((response) => {
      const res = response.data
      console.log(res)
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}
    getData()
  var header = <h1 className="text-title">Welcome!</h1>
  var desc1 = <h3 className="text-thin">This is a basic app.</h3>
  var desc2 = <h4 className="text-extrathin">Test out the buttons.</h4>
  
  function toconsole(whatToPrint){
    console.log(whatToPrint);
  }

  return(
    <div className="main">
      {header}
      {desc1}
      {desc2}
      <div className="buttonHolder">
        <Button
        text='button 1'
        func={() => getData()}/>
        <Button
        text='button 2'
        func={() => toconsole('Button 2 clicked!')}/>
        <Button
        text='button 3'
        func={() => toconsole('Button 3 clicked!')}/>
        </div>
      
    </div>
  );
}

export default App
