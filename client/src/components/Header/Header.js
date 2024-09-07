// src/components/Header.js
import React from "react";
import "./Header.css";

function Header() {
  return (
    <header className="header">
      <img src="/img/logo1.jpg" alt="Medical Illustration" />
      <div className="logo">
        <span className="health">Health</span>
        <span className="guard360">Guard360</span>
      </div>
      <nav className="nav">
        <a href="#locations">Locations</a>
        <a href="#doctors">Doctors</a>
        <a href="#treatments">Treatments</a>
        <a href="#diseases">Diseases</a>
      </nav>
    </header>
  );
}

export default Header;
