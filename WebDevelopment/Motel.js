// Author: Steven Norris
// About: Displaying the attributes of a motel guest utilizing object-oriented approach
// Date Created: 03/21/2024
// Date Modified: 03/24/2024

const motelCustomer = {
  // Customer personal information
  name: "Steven Norris",
  birthDate: new Date("1994-07-02"), // ISO format for dates
  gender: "Male",

  // Room preferences
  roomPreferences: ["Double Bed", "Pet-Friendly Status"],

  // Payment information
  paymentMethod: "Pennies",

  // Mailing address
  mailingAddress: {
    street: "123 Duck St",
    city: "St. John's",
    postalCode: "A5A 1A3",
    toString() {
      // Use of toString for cleaner output
      return `${this.street}, ${this.city}, ${this.postalCode}`;
    },
  },

  // Contact information
  phoneNumber: "709-987-6543",

  // Booking details
  checkInDate: new Date("2024-04-01"),
  checkOutDate: new Date("2024-04-15"),

  // Method to calculate the customer's age
  age: function () {
    const today = new Date();
    let age = today.getFullYear() - this.birthDate.getFullYear();
    const m = today.getMonth() - this.birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < this.birthDate.getDate())) {
      age--;
    }
    return age;
  },

  // Method to calculate the duration of stay in days
  durationOfStay: function () {
    const diffTime = Math.abs(
      this.checkOutDate.getTime() - this.checkInDate.getTime()
    );
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  },
};

// Prepares a descriptive paragraph based on the customers info
const customerDescription = `Hello! I'm ${
  motelCustomer.name
}, a ${motelCustomer.age()} year old ${
  motelCustomer.gender
} who prefers rooms with ${motelCustomer.roomPreferences.join(
  " and "
)}. You can reach me at ${
  motelCustomer.phoneNumber
}. My mailing address is ${motelCustomer.mailingAddress.toString()}. I'll be staying from ${motelCustomer.checkInDate.toLocaleDateString()} to ${motelCustomer.checkOutDate.toLocaleDateString()}, which is a duration of ${motelCustomer.durationOfStay()} days.`;

//Prints to the console
console.log(customerDescription);

// Finds the element with the ID 'customerInfo' and sets its text content
document.getElementById("customerInfo").textContent = customerDescription;
