document.addEventListener("DOMContentLoaded", () => {
    const openModalButton = document.getElementById("open-skill-modal");
    const closeModalButton = document.getElementById("close-skill-modal");
    const modal = document.getElementById("skill-modal");
    const skillForm = document.getElementById("skill-form");
    const skillIdField = document.getElementById("skill-id");
    const modalTitle = document.getElementById("skill-modal-title");

    const openModal = () => modal.classList.add("open");
    const closeModal = () => {
        modal.classList.remove("open");
        skillForm.reset();
        skillIdField.value = "";
        modalTitle.textContent = "Tambah Skill";
        skillForm.action = "/skills/add";
    };

    openModalButton?.addEventListener("click", openModal);
    closeModalButton?.addEventListener("click", closeModal);
    modal.addEventListener("click", (event) => {
        if (event.target === modal) closeModal();
    });

    document.querySelectorAll(".edit-skill").forEach((button) => {
        button.addEventListener("click", () => {
            const skillId = button.dataset.id;
            const nama = button.dataset.nama;
            const kategori = button.dataset.kategori;
            const persen = button.dataset.persen;

            skillIdField.value = skillId;
            modalTitle.textContent = "Edit Skill";
            skillForm.action = `/skills/${skillId}/edit`;
            skillForm.querySelector("#nama_skill").value = nama;
            skillForm.querySelector("#kategori_skill").value = kategori;
            skillForm.querySelector("#persentase_keahlian").value = persen;
            openModal();
        });
    });

    document.querySelectorAll("button[data-action='delete']").forEach((button) => {
        button.addEventListener("click", async () => {
            const skillId = button.dataset.id;
            const confirmed = confirm("Hapus skill ini?");
            if (!confirmed) return;

            try {
                const response = await fetch(`/skills/${skillId}/delete`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                });
                if (response.ok) {
                    location.reload();
                } else {
                    alert("Gagal menghapus skill. Silakan coba lagi.");
                }
            } catch (error) {
                alert("Terjadi kesalahan saat menghapus skill.");
            }
        });
    });
});