const revealItems = document.querySelectorAll(".reveal");

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  },
  { threshold: 0.18 }
);

revealItems.forEach((item) => observer.observe(item));

const filterChips = document.querySelectorAll(".filter-chip");
const projectCards = document.querySelectorAll(".project-card[data-category]");

filterChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    const selected = chip.dataset.filter;

    filterChips.forEach((item) => item.classList.toggle("active", item === chip));
    projectCards.forEach((card) => {
      const shouldShow = selected === "all" || card.dataset.category === selected;
      card.classList.toggle("is-hidden", !shouldShow);
    });
  });
});

const canvas = document.getElementById("constellation");
const ctx = canvas.getContext("2d");
let particles = [];

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  particles = Array.from({ length: Math.min(60, Math.floor(window.innerWidth / 22)) }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.4,
    vy: (Math.random() - 0.5) * 0.4,
    size: Math.random() * 2 + 0.8,
  }));
}

function drawParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  particles.forEach((particle, index) => {
    particle.x += particle.vx;
    particle.y += particle.vy;

    if (particle.x < 0 || particle.x > canvas.width) {
      particle.vx *= -1;
    }

    if (particle.y < 0 || particle.y > canvas.height) {
      particle.vy *= -1;
    }

    ctx.beginPath();
    ctx.fillStyle = "rgba(124, 199, 255, 0.8)";
    ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
    ctx.fill();

    for (let secondIndex = index + 1; secondIndex < particles.length; secondIndex += 1) {
      const neighbor = particles[secondIndex];
      const dx = particle.x - neighbor.x;
      const dy = particle.y - neighbor.y;
      const distance = Math.hypot(dx, dy);

      if (distance < 120) {
        ctx.beginPath();
        ctx.strokeStyle = `rgba(94, 234, 212, ${1 - distance / 120})`;
        ctx.lineWidth = 0.6;
        ctx.moveTo(particle.x, particle.y);
        ctx.lineTo(neighbor.x, neighbor.y);
        ctx.stroke();
      }
    }
  });

  requestAnimationFrame(drawParticles);
}

resizeCanvas();
drawParticles();
window.addEventListener("resize", resizeCanvas);
