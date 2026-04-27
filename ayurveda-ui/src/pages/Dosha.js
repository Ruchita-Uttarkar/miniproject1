import React, { useState } from "react";

export default function Dosha() {
  const [form, setForm] = useState({
    body: "",
    skin: "",
    digestion: "",
    sleep: ""
  });

  const [dosha, setDosha] = useState("");
  const [loading, setLoading] = useState(false);

  const remedies = {
    Vata: ["🌿 Ashwagandha", "🥛 Warm Milk", "💆 Oil Massage", "🧘 Meditation"],
    Pitta: ["🥥 Coconut Water", "🌱 Aloe Vera", "❄️ Cooling Diet", "🌸 Rose Water"],
    Kapha: ["🍵 Ginger Tea", "🍯 Honey", "🏃 Exercise", "🥗 Light Diet"]
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const predictDosha = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
      });

      const data = await res.json();
      setDosha(data.dosha);
    } catch {
      alert("Backend not connected");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-200 via-yellow-100 to-green-50 relative overflow-hidden">

      {/* 🌿 Background Glow */}
      <div className="absolute w-96 h-96 bg-green-300 opacity-30 rounded-full blur-3xl top-10 left-10"></div>
      <div className="absolute w-96 h-96 bg-yellow-200 opacity-30 rounded-full blur-3xl bottom-10 right-10"></div>

      {/* 🌿 Main Card */}
      <div className="backdrop-blur-xl bg-white/40 border border-white/30 shadow-2xl rounded-3xl p-8 w-full max-w-md space-y-5 z-10">

        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-green-900">
            🌿 Dosha Predictor
          </h1>
          <p className="text-gray-700 text-sm mt-1">
            Know your body type & balance your lifestyle
          </p>
        </div>

        {/* Form */}
        <select name="body" onChange={handleChange} className="input">
          <option value="">🧍 Body Type</option>
          <option>Thin</option>
          <option>Medium</option>
          <option>Heavy</option>
        </select>

        <select name="skin" onChange={handleChange} className="input">
          <option value="">💧 Skin Type</option>
          <option>Dry</option>
          <option>Normal</option>
          <option>Oily</option>
        </select>

        <select name="digestion" onChange={handleChange} className="input">
          <option value="">🔥 Digestion</option>
          <option>Irregular</option>
          <option>Strong</option>
          <option>Slow</option>
        </select>

        <select name="sleep" onChange={handleChange} className="input">
          <option value="">🌙 Sleep Pattern</option>
          <option>Light</option>
          <option>Moderate</option>
          <option>Heavy</option>
        </select>

        {/* Button */}
        <button
          onClick={predictDosha}
          className="w-full py-3 rounded-xl text-white font-semibold bg-gradient-to-r from-green-600 to-green-800 hover:scale-105 transition duration-300 shadow-lg"
        >
          {loading ? "🌿 Analyzing..." : "✨ Predict Dosha"}
        </button>

        {/* Result */}
        {dosha && (
          <div className="mt-4 p-4 bg-white/70 rounded-xl shadow-inner animate-fade">
            <h2 className="text-xl font-bold text-green-800 text-center">
              🌸 Your Dosha: {dosha}
            </h2>

            <ul className="mt-3 space-y-2">
              {remedies[dosha].map((item, i) => (
                <li key={i} className="bg-green-50 p-2 rounded-lg">
                  {item}
                </li>
              ))}
            </ul>
          </div>
        )}

      </div>
    </div>
  );
}  