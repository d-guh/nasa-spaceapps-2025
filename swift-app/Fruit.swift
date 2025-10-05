//
//  Fruit.swift
//  SpaceApps
//
//  Created by Julia Holzbach on 10/4/25.
//

import Foundation
import SwiftUI

struct Fruit: Hashable, Identifiable {
    let name: String
    let growthToMaturity: Int
    let plantDate: Date
    var timeLeft: Int
    var status: Status
   
    let id = UUID()
    
    enum Status {
        case wait
        case grow
        case plant
    }
    
    init(name: String, growthToMaturity: Int, plantDate: Date, status: Status, timeLeft: Int) {
        self.name = name
        self.growthToMaturity = growthToMaturity
        self.plantDate = plantDate
        self.status = status
        self.timeLeft = timeLeft
    }
    
    func whenToPlant() -> Date? {
        let bloomDate = Date()
        let plantDate = Calendar.current.date(byAdding: .day, value: -growthToMaturity, to: bloomDate)
    
        return plantDate
    }
     
    func howManyDaysToPlant() -> Int? {
        let currentDate = Date()
        guard let plantDate = whenToPlant() else { return 0 }
        let diffInDays = Calendar.current.dateComponents([.day], from: currentDate, to: plantDate).day
        
        return diffInDays
    }
    
    
}
