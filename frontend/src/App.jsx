import React,{useState} from "react"
import Button from "./Button.jsx"

function App() {
  var header = <h1 className="text-title">Welcome!</h1>
  var desc1 = <h3 className="text-thin">This is a basic app.</h3>
  var desc2 = <h4 className="text-extrathin">Test out the buttons.</h4>
  
  return(
    <div className="main">
      {header}
      {desc1}
      {desc2}
      <Button/>
    </div>
  );
}

export default App
