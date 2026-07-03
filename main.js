// ==========================================================
// 1. تأثير الكتابة التلقائية (Typing Effect)
// ==========================================================
const highlightText = document.querySelector('.hero-content h1 .highlight');
const words = ["الأتمتة والذكاء", "أكواد المستقبل", "أدوات الـ ERP"];
let wordIndex = 0;
let charIndex = 0;
let isDeleting = false;

function typeEffect() {
    const currentWord = words[wordIndex];
    
    if (isDeleting) {
        highlightText.textContent = currentWord.substring(0, charIndex - 1);
        charIndex--;
    } else {
        highlightText.textContent = currentWord.substring(0, charIndex + 1);
        charIndex++;
    }

    let typeSpeed = isDeleting ? 50 : 100;

    if (!isDeleting && charIndex === currentWord.length) {
        typeSpeed = 2000; 
        isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        wordIndex = (wordIndex + 1) % words.length;
        typeSpeed = 500; 
    }

    setTimeout(typeEffect, typeSpeed);
}

// ==========================================================
// 2. تأثير العداد التفاعلي (Animated Counters)
// ==========================================================
const counters = document.querySelectorAll('.stat-number');
const speed = 150; 

const startCounters = () => {
    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText.replace('%', '').replace('+', '');
            const inc = target / speed;

            if (count < target) {
                const current = Math.ceil(count + inc);
                counter.innerText = current;
                setTimeout(updateCount, 10);
            } else {
                counter.innerText = target + (target === 100 ? '%' : '+');
            }
        };
        updateCount();
    });
};

// ==========================================================
// 3. تأثير السكرول والتكشف التدريجي (Scroll Reveal)
// ==========================================================
const sections = document.querySelectorAll('.service-card, .about-text, .stat-box, .contact-form');

const revealOnScroll = () => {
    const triggerBottom = window.innerHeight * 0.95;

    sections.forEach(section => {
        const sectionTop = section.getBoundingClientRect().top;
        if (sectionTop < triggerBottom) {
            section.classList.add('active-reveal');
        }
    });

    const aboutSection = document.querySelector('.about-section');
    if(aboutSection) {
        const aboutTop = aboutSection.getBoundingClientRect().top;
        if (aboutTop < triggerBottom && !triggered) {
            startCounters();
            triggered = true;
        }
    }
};

let triggered = false;
window.addEventListener('scroll', revealOnScroll);

// ==========================================================
// 4. تأثير الماوس ثلاثي الأبعاد على الكروت (3D Tilt Effect)
// ==========================================================
const cards = document.querySelectorAll('.service-card');

cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const cardRect = card.getBoundingClientRect();
        const cardWidth = cardRect.width;
        const cardHeight = cardRect.height;
        
        const mouseX = e.clientX - cardRect.left - cardWidth / 2;
        const mouseY = e.clientY - cardRect.top - cardHeight / 2;
        
        const rotateX = -(mouseY / cardHeight / 2) * 15;
        const rotateY = (mouseX / cardWidth / 2) * 15;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-5px)`;
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)`;
    });
});

// ==========================================================
// 5. التحكم في نموذج التواصل (Contact Form)
// ==========================================================
const form = document.getElementById('contact-form');
if(form) {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const submitBtn = form.querySelector('button');
        submitBtn.innerText = "جاري الإرسال بذكاء...";
        submitBtn.disabled = true;

        setTimeout(() => {
            submitBtn.innerText = "تمت العملية بنجاح! ✓";
            submitBtn.style.background = "#10b981"; 
            form.reset();
        }, 1500);
    });
}

// ==========================================================
// 6. إدارة الجلسة وعرض اسم العميل المحدث في الهيدر
// ==========================================================
document.addEventListener("DOMContentLoaded", () => {
    // تشغيل تأثيرات الواجهة الأساسية
    typeEffect();
    counters.forEach(c => c.innerText = "0");
    setTimeout(revealOnScroll, 100); 

    // فحص جلسة العميل الحالي
    const currentClientName = localStorage.getItem("currentClientName");
    const navLinks = document.querySelector(".nav-links");
    const clientBtn = document.querySelector(".btn-nav");

    if (currentClientName && navLinks && clientBtn) {
        // إخفاء زر بوابة العملاء القديم
        clientBtn.style.display = "none";

        // إنشاء عنصر جديد مخصص لعرض اسم العميل وزر الخروج بنظام النيون
        const clientInfo = document.createElement("div");
        clientInfo.className = "client-user-info";
        clientInfo.style.display = "inline-flex";
        clientInfo.style.alignItems = "center";
        clientInfo.style.gap = "15px";

        clientInfo.innerHTML = `
            <span style="color: var(--primary); font-weight: 700; font-size: 16px;">👋 ${currentClientName}</span>
            <a href="#" id="logout-btn" style="color: #ef4444; text-decoration: none; font-size: 14px; font-weight: 700; border: 1px solid #ef4444; padding: 4px 14px; border-radius: 50px; transition: 0.3s; background: rgba(239, 68, 68, 0.05);">خروج</a>
        `;

        navLinks.appendChild(clientInfo);

        // منطق تسجيل الخروج المباشر
        document.getElementById("logout-btn").addEventListener("click", (e) => {
            e.preventDefault();
            localStorage.removeItem("currentClientName"); // حذف العميل الحالي من الجلسة
            alert("تم تسجيل الخروج من المنصة بنجاح.");
            window.location.reload(); // تحديث فوري لإعادة زر الدخول
        });
    }
});