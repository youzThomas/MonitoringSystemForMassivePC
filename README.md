# Monitoring System for Massive PC (MSMP)

**MSMP** is a lightweight access control system designed to manage public or lab computers through a time-based reservation mechanism. It ensures that each workstation can only be accessed by authorized users during their assigned time slots, helping prevent misuse, unauthorized access, and overtime occupancy.

The system consists of a frontend reservation portal, a backend API service, and a client-side agent that enforces screen locking and credential verification.

## Features

- Full-screen lock enforcement on Windows client
- Credential verification during valid reservation period
- Web-based reservation system (Vue 3 + TailwindCSS)
- Lightweight Flask API server for reservation logic
- Deployable on Render for free

## Project Structure

