function menu_bar_transform(x) {
    x.classList.toggle("change"); // this changes the shape of the hamburger-like button to an X, as defined in the csv
    const links = document.getElementById("internal_links");
    const menu = document.getElementById("menu");

    if (links.classList.contains("fade-in")) { // this fades out the menu if it's faded in, or fades in the menu if it's not faded in
        // here the menu is faded out
        links.classList.remove("fade-in");
        links.classList.remove("pre-fade-in");
        links.classList.add("fade-out");
        menu.style.marginTop = "0" ; 
        console.log(`fade-out triggered`);
    } else {
        // here the menu is faded in
        links.classList.remove("fade-out");
        links.classList.add("pre-fade-in"); // here I'm making it take up space but remain hidden, to leave space for the animation
        menu.style.marginTop = "20px" ; // I'm adding a margin to keep a gap between the logo and the menu
        console.log(`pre-fade-in triggered`);

        // I'm setting a very small delay to allow the browser to process the display change, 
        // so that it starts the fade-in animation after changing the display style to make space for the menu animation
        setTimeout(() => {
            links.classList.add("fade-in"); // this starts the fade-in animation
            links.classList.remove("pre-fade-in");
            menu.style.marginTop = "20px" ;
            console.log(`fade-in triggered`);
        }, 10);
    }
}