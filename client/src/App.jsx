import { BrowserRouter as Router,Routes,Route} from 'react-router-dom'
import './App.css'
import Home from './pages/Home'
import About from './pages/About'
import Graph from './pages/Graph'
import Insights from './pages/Insights' 
function App() {

  return (
    <>
    <Router>
      <Routes>
      <Route path="/" element={<Home/>} />
      <Route path="/about" element={<About/>} />
      <Route path="/generate-graph" element={<Graph/>} />
      <Route path="/extract-insight" element={<Insights/>} />
      </Routes>
    </Router>

    </>
  )
}

export default App
