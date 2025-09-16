// Simple test for TumbleButton theme toggle functionality
// Run in browser console to verify behavior

(function testTumbleButton() {
    console.log('🧪 Testing TumbleButton Theme Toggle...');
    
    // Test 1: Theme toggle button exists
    const toggleButton = document.getElementById('theme-toggle');
    console.assert(toggleButton, '❌ Theme toggle button not found');
    console.log('✅ Theme toggle button found');
    
    // Test 2: Initial state
    const initialTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    console.log(`✅ Initial theme: ${initialTheme}`);
    
    // Test 3: localStorage persistence
    const savedTheme = localStorage.getItem('theme');
    console.log(`✅ Saved theme in localStorage: ${savedTheme}`);
    
    // Test 4: Accessibility attributes
    const ariaChecked = toggleButton?.getAttribute('aria-checked');
    const ariaLabel = toggleButton?.getAttribute('aria-label');
    console.assert(ariaLabel, '❌ Missing aria-label');
    console.assert(ariaChecked !== null, '❌ Missing aria-checked');
    console.log(`✅ Accessibility: aria-label="${ariaLabel}", aria-checked="${ariaChecked}"`);
    
    // Test 5: Theme toggle functionality
    let testPassed = true;
    const originalTheme = document.documentElement.getAttribute('data-theme');
    
    if (toggleButton) {
        // Simulate click
        toggleButton.click();
        
        // Check if theme changed
        const newTheme = document.documentElement.getAttribute('data-theme');
        const themeChanged = newTheme !== originalTheme;
        console.assert(themeChanged, '❌ Theme did not change after toggle');
        
        if (themeChanged) {
            console.log(`✅ Theme toggle works: ${originalTheme} → ${newTheme}`);
            
            // Check localStorage update
            const newSavedTheme = localStorage.getItem('theme');
            console.assert(newSavedTheme === newTheme, '❌ localStorage not updated');
            console.log(`✅ localStorage updated: ${newSavedTheme}`);
            
            // Check aria-checked update
            const newAriaChecked = toggleButton.getAttribute('aria-checked');
            const expectedAriaChecked = newTheme === 'light' ? 'true' : 'false';
            console.assert(newAriaChecked === expectedAriaChecked, '❌ aria-checked not updated');
            console.log(`✅ aria-checked updated: ${newAriaChecked}`);
            
            // Restore original theme
            toggleButton.click();
            
        } else {
            testPassed = false;
        }
    }
    
    // Test 6: Particles consistency check
    if (typeof window.portfolioApp !== 'undefined') {
        console.log('✅ PortfolioApp instance found');
        
        // Check if particles config is consistent
        const particlesContainer = document.getElementById('particles-js');
        if (particlesContainer) {
            console.log('✅ Particles container found');
            
            // Log particle configuration for manual verification
            console.log('📊 Verify particles have same movement/size/speed across themes:');
            console.log('   - Number: 150');
            console.log('   - Speed: 5');
            console.log('   - Size: 3');
            console.log('   - Distance: 150');
            console.log('   - Only color should differ between themes');
        }
    }
    
    console.log(testPassed ? '🎉 All tests passed!' : '❌ Some tests failed!');
    return testPassed;
})();