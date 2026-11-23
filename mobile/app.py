import flet as ft
import httpx

# Use 127.0.0.1 since Flet and FastAPI are running on the same phone
API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    page.title = "IEYFWW"
    page.bgcolor = "#0B6E4F" # Deep Green
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # UI Elements
    title = ft.Text("IEYFWW", size=40, weight=ft.FontWeight.BOLD, color="white")
    subtitle = ft.Text("Ikot Ese Youth Foundation Worldwide", color="#FFC107", size=14)
    
    phone_input = ft.TextField(
        label="Phone Number (e.g. 08012345678)", 
        border_color="#FFC107",
        color="white",
        label_style=ft.TextStyle(color="white")
    )
    
    otp_input = ft.TextField(
        label="Enter OTP", 
        border_color="#FFC107",
        color="white",
        label_style=ft.TextStyle(color="white"),
        visible=False
    )
    
    status_text = ft.Text("", color="red", size=14)

    # Button Actions
    def send_otp_click(e):
        status_text.value = "Sending OTP..."
        page.update()
        
        try:
            # Call your FastAPI backend
            response = httpx.post(f"{API_URL}/auth/send-otp", json={"phone": phone_input.value})
            
            if response.status_code == 200:
                status_text.value = "OTP Sent! Check your SMS."
                status_text.color = "white"
                otp_input.visible = True
                send_btn.visible = False
                verify_btn.visible = True
            else:
                status_text.value = response.json().get("detail", "Error sending OTP")
                status_text.color = "red"
        except Exception as ex:
            status_text.value = f"Connection error: {ex}"
            status_text.color = "red"
        page.update()

    def verify_otp_click(e):
        status_text.value = "Verifying..."
        page.update()
        
        try:
            response = httpx.post(f"{API_URL}/auth/verify-otp", json={
                "phone": phone_input.value,
                "token": otp_input.value
            })
            
            if response.status_code == 200:
                status_text.value = "Login Successful! Welcome to IEYFWW."
                status_text.color = "#FFC107"
                # Later we will navigate to the main chat screen here
            else:
                status_text.value = response.json().get("detail", "Invalid OTP")
                status_text.color = "red"
        except Exception as ex:
            status_text.value = f"Connection error: {ex}"
            status_text.color = "red"
        page.update()

    send_btn = ft.ElevatedButton(
        text="Send OTP", 
        on_click=send_otp_click, 
        bgcolor="#FFC107", 
        color="#0B6E4F",
        width=200
    )
    
    verify_btn = ft.ElevatedButton(
        text="Verify OTP", 
        on_click=verify_otp_click, 
        bgcolor="#FFC107", 
        color="#0B6E4F",
        width=200,
        visible=False
    )

    # Add everything to the screen
    page.add(
        ft.Column([
            title,
            subtitle,
            ft.Divider(height=40, color="transparent"),
            phone_input,
            send_btn,
            otp_input,
            verify_btn,
            status_text
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

# THE FIX IS HERE: Changed ft.app to ft.run
ft.run(main)
