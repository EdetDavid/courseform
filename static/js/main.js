// Ensure this code runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get the tab links and tab panes
    var studentTab = document.getElementById('student-tab');
    var hodTab = document.getElementById('hod-tab');
    var studentLogin = document.getElementById('studentLogin');
    var hodLogin = document.getElementById('hodLogin');
  
    // Function to show the selected tab
    function showTab(tabToShow) {
      // Hide both panes
      studentLogin.classList.remove('show', 'active');
      hodLogin.classList.remove('show', 'active');
  
      // Show the selected pane
      tabToShow.classList.add('show', 'active');
    }
  
    // Event listeners for tab clicks
    studentTab.addEventListener('click', function() {
      showTab(studentLogin);
    });
  
    hodTab.addEventListener('click', function() {
      showTab(hodLogin);
    });
  
    // Show the Student tab by default (you can change this if needed)
    showTab(studentLogin);
  });
  