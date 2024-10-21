import { Fragment } from "react";
import NavBar from "./components/NavBar";
import Presentations from "./pages/Presentations";

function App() {
  return (
    <Fragment>
      <NavBar />
      <Presentations />
    </Fragment>
  );
}

export default App;
