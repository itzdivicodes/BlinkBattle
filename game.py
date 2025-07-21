import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import time
import threading
from PIL import Image, ImageTk
from blink import BlinkDetector

class DontBlinkGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Don't Blink Game")
        self.root.geometry("800x650")
        self.root.configure(bg='#2c3e50')
        
        # Initialize variables
        self.cap = None
        self.blink_detector = BlinkDetector()
        self.game_running = False
        self.start_time = None
        self.current_time = 0.0
        self.game_ended = False
        self.last_blink_count = 0
        
        # Setup UI
        self.setup_ui()
        
        # Start camera automatically
        self.start_camera()
        
    def setup_ui(self):
        """Setup the clean UI layout"""
        # Timer at the top
        self.timer_label = tk.Label(self.root, text="Time: 0.00s", 
                                  font=('Arial', 32, 'bold'),
                                  fg='#e74c3c', bg='#2c3e50')
        self.timer_label.pack(pady=20)
        
        # Video frame
        self.video_frame = tk.Label(self.root, bg='#34495e', 
                                   width=640, height=480,
                                   text="Camera Starting...",
                                   font=('Arial', 16),
                                   fg='#95a5a6')
        self.video_frame.pack(pady=10)
        
        # Single button
        self.game_button = tk.Button(self.root, text="START", 
                                   command=self.toggle_game,
                                   font=('Arial', 20, 'bold'),
                                   bg='#27ae60', fg='white',
                                   width=15, height=2)
        self.game_button.pack(pady=30)
        
    def start_camera(self):
        """Start camera automatically"""
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            # Turn off all debug displays
            self.blink_detector.debug_mode = False
            self.blink_detector.reset_blink_counter()
            self.update_video()
        else:
            messagebox.showerror("Error", "Could not access camera!")
            
    def update_video(self):
        """Update video feed continuously"""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Only process for blink detection if game is running
                if self.game_running and not self.game_ended:
                    blink_detected, frame, ear_value = self.blink_detector.detect_blink_clean(frame)
                    
                    # Update timer
                    self.update_timer()
                    
                    # Check for NEW blink
                    current_blink_count = self.blink_detector.total_blinks
                    if current_blink_count > self.last_blink_count:
                        self.last_blink_count = current_blink_count
                        self.end_game()
                else:
                    # Just show clean video feed when game not running
                    pass  # No processing needed, just show raw video
                
                # Convert frame to display format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                frame_pil = frame_pil.resize((640, 480), Image.Resampling.LANCZOS)
                frame_tk = ImageTk.PhotoImage(frame_pil)
                
                self.video_frame.configure(image=frame_tk, text='')
                self.video_frame.image = frame_tk
        
        # Schedule next update
        if self.cap:
            self.root.after(30, self.update_video)
    
    def toggle_game(self):
        """Toggle between start game and play again"""
        if not self.game_running and not self.game_ended:
            self.start_game()
        else:
            self.reset_game()
    
    def start_game(self):
        """Start the game"""
        self.game_running = True
        self.game_ended = False
        self.start_time = time.time()
        self.current_time = 0.0
        
        # Reset blink detector
        self.blink_detector.reset_blink_counter()
        self.last_blink_count = 0
        
        # Update UI
        self.game_button.configure(text="RUNNING...", state='disabled', bg='#95a5a6')
        self.timer_label.configure(fg='#27ae60')
    
    def end_game(self):
        """End the game"""
        if self.game_running:
            self.game_running = False
            self.game_ended = True
            
            # Update UI
            self.game_button.configure(text="PLAY AGAIN", state='normal', bg='#f39c12')
            self.timer_label.configure(fg='#e74c3c')
            
            # Show result message
            messagebox.showinfo("Game Over", 
                              f"You blinked!\n\nTime: {self.current_time:.2f} seconds")
    
    def reset_game(self):
        """Reset the game for play again"""
        self.game_running = False
        self.game_ended = False
        self.start_time = None
        self.current_time = 0.0
        
        # Reset blink detector
        self.blink_detector.reset_blink_counter()
        self.last_blink_count = 0
        
        # Reset UI
        self.game_button.configure(text="START", bg='#27ae60')
        self.timer_label.configure(text="Time: 0.00s", fg='#e74c3c')
    
    def update_timer(self):
        """Update the game timer"""
        if self.game_running and self.start_time and not self.game_ended:
            self.current_time = time.time() - self.start_time
            self.timer_label.configure(text=f"Time: {self.current_time:.2f}s")
    
    def on_closing(self):
        """Handle window closing"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

def main():
    root = tk.Tk()
    game = DontBlinkGame(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", game.on_closing)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
