import { useNavigate } from "react-router-dom";

export default function Signup() {
  const nav = useNavigate();

  return (
    <div style={{ textAlign: "center", padding: 100 }}>
      <h2>Signup</h2>

      <input placeholder="Name" /><br /><br />
      <input placeholder="Email" /><br /><br />
      <input type="password" placeholder="Password" /><br /><br />

      <button onClick={() => nav("/")}>Register</button>
    </div>
  );
}
