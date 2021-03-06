const searchForm = document.querySelector("#searchForm");
const pageLinks = document.querySelectorAll(".page-link");
const tags = document.getElementsByClassName("project-tag");
const BASE_URL = "https://adev-devsearch.herokuapp.com/";

if (searchForm) {
	for (let i = 0; pageLinks.length > i; i++) {
		pageLinks[i].addEventListener("click", function (e) {
			e.preventDefault();

			let page = this.dataset.page;

			searchForm.innerHTML += `<input value=${page} name="page" hidden />`;
			searchForm.submit();
		});
	}
}

for (let i = 0; tags.length > i; i++) {
	tags[i].addEventListener("click", (e) => {
		let tagId = e.target.dataset.tag;
		let projectId = e.target.dataset.project;

		fetch(`${BASE_URL}api/remove-tag`, {
			method: "DELETE",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ project: projectId, tag: tagId }),
		})
			.then((res) => res.json())
			.then((data) => {
				e.target.remove();
			});
	});
}
