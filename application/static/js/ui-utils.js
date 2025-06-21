function countUp(element, target) {
    const startTime = performance.now();
    const duration = 1300; // milliseconds

    function update(timestamp) {
        // Calculate normalized progress [0..1]
        const elapsed = timestamp - startTime;
        let progress = Math.min(elapsed / duration, 1);

        // Ease-out
        progress = 1 - (1 - progress) * (1 - progress);

        // Update the element's text
        element.textContent = Math.floor(target * progress);

        // Keep animating until we reach the end
        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = target; // Ensure final value is exact
        }
    }

    requestAnimationFrame(update);
}